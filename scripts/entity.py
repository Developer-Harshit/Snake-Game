from random import choice, randint
from scripts.utils import add_vector


class Player:
    def __init__(self, game):
        self.game = game
        self.pos = choice(list(self.game.tilemap.map.values())).pos

        self.direction = [0, 0]

    def get_global_pos(self, loc, offset=(0, 0)):
        return (
            loc[0] * self.game.size + offset[0],
            loc[1] * self.game.size + offset[1],
        )

    def render(self, surf):
        surf.blit(self.game.assets["head"], self.get_global_pos(self.pos))

    def change_direction(self, direction):
        self.direction = direction

    def update(self):
        self.pos = add_vector(self.direction, self.pos)
