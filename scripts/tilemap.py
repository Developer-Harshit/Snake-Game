from random import random, choice, randint
from scripts.utils import load_image, load_images
from perlin_noise import PerlinNoise


def loc_to_str(x, y):
    return str(x) + ";" + str(y)


class Tile:
    def __init__(self, pos, t_type, variant):
        self.pos = tuple(pos)
        self.type = t_type
        self.variant = variant

    def get_object(self):
        return {"pos": self.pos, "type": self.type, "variant": self.variant}


class Tilemap:
    def __init__(self, game):
        self.game = game

        # formap of map -------> {'x;y':tileObj,'0;6':tileObj,............}
        self.map = {}

    def get_global_pos(self, loc, offset=(0, 0)):
        return (
            loc[0] * self.game.size + offset[0],
            loc[1] * self.game.size + offset[1],
        )

    def create_random(self, w, h):
        self.map = {}
        rows = int(w / self.game.size)
        cols = int(h / self.game.size)

        noise = PerlinNoise(1, randint(20, 1000))
        xoff = randint(20, 10000)
        for j in range(0, cols):
            xoff += 0.1
            yoff = 0
            var_list = [0, 1, 2, 0, 0, 0, 1, 2, 1, 0, 0, 1]
            for i in range(0, rows):
                yoff += 0.1
                n_index = int((abs(noise((xoff, yoff)))) * len(var_list))

                tile_var = var_list[n_index]
                self.map[loc_to_str(i, j)] = Tile((i, j), "tiles", tile_var)

    def render(self, surf):
        for tile in self.map.values():
            myImg = self.game.assets[tile.type][tile.variant]
            surf.blit(myImg, self.get_global_pos(tile.pos))
