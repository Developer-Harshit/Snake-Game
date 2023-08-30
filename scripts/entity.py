from random import choice, randint
from scripts.utils import add_vector
import pygame


class Block:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)

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
    def __init__(self, game, pos, e_type, u_time=10, t_count=0):
        super().__init__(game, pos)
        self.type = e_type

        self.direction = [0, 0]
        self.rotate = 0
        self.update_time = u_time
        self.tail = Tail(self, game, t_count)

    def render(self, surf, offset=[0, 0]):
        self.tail.render(surf, offset)
        img = pygame.transform.rotate(self.game.assets[self.type], self.rotate)

        super().render(surf, img, offset)

    def update(self, frame):
        if frame % self.update_time == 0 and not self.check_tile_collision():
            self.tail.update()

            self.pos = add_vector(self.pos, self.direction)

            return True
        return False

    def check_tile_collision(self):
        c_pos = self.game.tilemap.get_collision_pos()
        if add_vector(self.direction, self.pos) in c_pos:
            return True
        return False

    def change_direction(self, direction=[0, 0]):
        self.direction = direction
        if direction[0] > 0:
            self.rotate = 90
        elif direction[0] < 0:
            self.rotate = 270
        elif direction[1] < 0:
            self.rotate = 180
        else:
            self.rotate = 0

    def add_tail(self, amount=1):
        self.tail.count += amount


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
        if len(self.tail) >= self.count:
            self.tail.pop(0)

        if len(self.tail) < self.count:
            self.tail.append(Block(self.game, self.host.pos))

    def render(self, surf, offset):
        for block in self.tail:
            block.render(surf, self.game.assets["tail"], offset)
