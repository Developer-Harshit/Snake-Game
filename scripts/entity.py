from random import choice, randint, random
from scripts.utils import add_vector, remap
import pygame


def loc_to_str(vect):
    return str(vect[0]) + ";" + str(vect[1])


class Tail:
    def __init__(self, host, game, t_count):
        self.host = host
        self.game = game
        self.tail = []

        self.count = t_count

    def get_global_pos(self, loc, offset=[0, 0]):
        return (
            loc[0] * self.game.size - offset[0],
            loc[1] * self.game.size - offset[1],
        )

    # Execute it before updating host
    def update(self):
        if len(self.tail) < self.count:
            self.tail.append(Block(self.game, self.host.pos))
        if len(self.tail) >= self.count and self.count:
            self.tail.pop(0)

    def render(self, surf, offset):
        img = self.game.assets[(self.host.type + "/" + "tail")]

        for block in self.tail:
            block.render(surf, img, offset)


class Block:
    def __init__(self, game, pos):
        self.game = game
        self.pos = tuple(pos)

    def get_global_pos(self, offset=(0, 0)):
        return (
            (self.pos[0] * self.game.size) - offset[0],
            (self.pos[1] * self.game.size) - offset[1],
        )

    def get_rect(self):
        pos = self.get_global_pos()
        return pygame.Rect(pos[0], pos[1], self.game.size, self.game.size)

    def is_colliding(self, other):
        if list(self.pos) == list(other.pos):
            return True
        return False

    def render(self, surf, img, offset=[0, 0]):
        surf.blit(img, (self.get_global_pos(offset)))


class Entity(Block):
    def __init__(self, game, pos, e_type, u_time=20, t_count=0):
        super().__init__(game, pos)
        self.type = e_type

        self.direction = [0, 0]
        self.rotate = 0
        self.update_time = u_time
        self.tail = Tail(self, game, t_count)
        self.death = 0

    def render(self, surf, offset=[0, 0]):
        img = pygame.transform.rotate(
            self.game.assets[self.type + "/" + "head"], self.rotate
        )

        super().render(surf, img, offset)

    def update(self, frame):
        if frame % self.update_time == 0 and not self.check_tile_collision():
            self.tail.update()
            self.change_rotation()
            self.pos = add_vector(self.pos, self.direction)
            return True
        return False

    def check_tile_collision(self):
        c_pos = self.game.tilemap.get_collision_pos()
        my_pos = tuple(add_vector(self.direction, self.pos))
        if my_pos in c_pos or my_pos in self.game.collide_pos:
            self.death += 1
            return True

        return False

    def change_direction(self, direction=[0, 0]):
        self.direction = direction

    def change_rotation(self):
        if self.direction[0] > 0:
            self.rotate = 90
        elif self.direction[0] < 0:
            self.rotate = 270
        elif self.direction[1] < 0:
            self.rotate = 180
        else:
            self.rotate = 0

    def add_tail(self, amount=1):
        self.tail.count += amount


class Enemy(Entity):
    def __init__(self, game, e_type, pos):
        super().__init__(game, pos, e_type, 13, 0)

        # for A-Star
        self.nodemap = self.game.tilemap.copy()
        self.reset_astar()

    def reset_astar(self):
        self.start = self.nodemap.map[loc_to_str(self.pos)]
        self.goal = self.nodemap.map[loc_to_str(self.game.player.pos)]
        self.nodemap.reset_cost()

        self.start.g, self.openset, self.closeset, self.cameFrom = (
            0,
            [self.start],
            [],
            {},
        )

    def change_direction(self, my_path):
        if len(my_path) > 1:
            n_pos = list(my_path[1].pos)
            x = n_pos[0] - self.pos[0]
            if x != 0:
                x = x // abs(x)
            y = n_pos[1] - self.pos[1]
            if y != 0:
                y = y // abs(y)
            self.direction = [x, y]
        else:
            return False

    def update(self, frame):
        dist = (
            (self.goal.pos[0] - self.pos[0]) ** 2
            + (self.goal.pos[1] - self.pos[1]) ** 2
        ) ** 0.5

        if dist < 25 and random() > 0.3:
            i = 0
            while 1:
                if i > 100:
                    break
                i += 1

                my_path = self.a_star()

                if my_path:
                    self.change_direction(my_path)

                    break

        if super().update(frame):
            self.reset_astar()
            pass

    def reconstruct(self, current):
        path = [current]

        while loc_to_str(current.pos) in self.cameFrom:
            current = self.cameFrom[loc_to_str(current.pos)]
            path.insert(0, current)

        return path

        pass

    def get_current(self):
        current = False
        for node in self.openset:
            node.heuristics(self.goal)
            if current:
                if current.f > node.f:
                    current = node
            else:
                current = node
        return current

    def a_star(self):
        if len(self.openset) == 0:
            print("No Solution")
            self.death += 1
            return False
        else:
            current = self.get_current()
            if current == self.goal:
                return self.reconstruct(current)
            self.openset.remove(current)
            self.closeset.append(current)

            for neighbor in current.get_neighbours(self.nodemap.map):
                if neighbor.type == "wall":
                    continue
                if tuple(neighbor.pos) in self.game.collide_pos:
                    continue

                tentG = current.g + 1
                if tentG < neighbor.g:
                    self.cameFrom[loc_to_str(neighbor.pos)] = current
                    neighbor.g = tentG
                    neighbor.f = tentG + neighbor.heuristics(self.goal)
                if neighbor not in self.openset:
                    if neighbor not in self.closeset:
                        self.openset.append(neighbor)
        return False


class Player(Entity):
    def __init__(self, game, pos):
        super().__init__(game, pos, "player", 12, 5)
        self.dashing = 0

    def update(self, frame):
        self.dashing = max(0, self.dashing - 1)

        if self.dashing > 10:
            self.update_time = 2
        else:
            self.update_time = 12

        super().update(frame)

    def dash(self):
        if self.dashing <= 0 and len(self.tail.tail) > 1:
            self.dashing = 24
            self.tail.count = max(self.tail.count - 1, 1)

            return True

        pass

    def shoot(self):
        pass

    def ghost(self):
        pass
