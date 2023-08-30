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


class Tail:
    def __init__(self, host, game):
        self.host = host
        self.game = game
        self.tail = []

        self.count = 1

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
            self.tail.append(Block(self.game, self.host.block.pos))

    def render(self, surf, offset):
        for block in self.tail:
            block.render(surf, self.game.assets["tail"], offset)

            # surf.blit(self.game.assets["tail"], self.get_global_pos(pos))


class Player:
    def __init__(self, game):
        self.game = game

        my_pos = choice(list(self.game.tilemap.map.values())).pos
        self.block = Block(game, my_pos)

        self.tail = Tail(self, self.game)
        self.direction = [0, 0]

    def get_global_pos(self, loc, offset=(0, 0)):
        return (
            loc[0] * self.game.size + offset[0],
            loc[1] * self.game.size + offset[1],
        )

    def check_tile_collision(self):
        c_pos = self.game.tilemap.get_collision_pos()
        if add_vector(self.direction, self.block.pos) in c_pos:
            print("collision")

    def render(self, surf, offset=[0, 0]):
        self.tail.render(surf, offset)
        self.block.render(surf, self.game.assets["player"], offset)

    def change_direction(self, direction):
        self.direction = direction

    def update(self):
        self.tail.update()
        self.check_tile_collision()
        self.block.pos = add_vector(self.direction, self.block.pos)
