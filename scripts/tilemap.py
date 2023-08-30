from random import random, choice, randint
from scripts.utils import load_image, load_images
from perlin_noise import PerlinNoise

COLLISION_TILES = ["wall"]


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
        self.zoff = 100
        self.noise = PerlinNoise(1, randint(20, 1000))

    def get_global_pos(self, loc, offset=(0, 0)):
        return (
            loc[0] * self.game.size - offset[0],
            loc[1] * self.game.size - offset[1],
        )

    def get_collision_pos(self):
        result = []
        for tile in self.map.values():
            if tile.type in COLLISION_TILES:
                result.append(tile.pos)
        return result

    def create_random(self, w, h):
        self.map = {}
        rows = int(w / self.game.size)
        cols = int(h / self.game.size)

        xoff = 10000
        self.zoff += 0.1

        for j in range(0, cols):
            xoff += 0.1
            yoff = 0
            var_list = [0, 1, 2, 0, 0, 0, 1, 2, 1, 0, 0, 1, 2, 0, 0, 1]
            for i in range(0, rows):
                if i == 0 or j == 0 or j == cols - 1 or i == rows - 1:
                    self.map[loc_to_str(i, j)] = Tile((i, j), "wall", 0)
                    continue
                yoff += 0.1
                n_index = int(
                    (abs(self.noise((xoff, yoff, self.zoff)))) * len(var_list)
                )

                tile_var = var_list[n_index]

                self.map[loc_to_str(i, j)] = Tile((i, j), "ground", tile_var)

    def render(self, surf, offset=[0, 0]):
        for tile in self.map.values():
            myImg = self.game.assets[tile.type][tile.variant]
            surf.blit(myImg, self.get_global_pos(tile.pos, offset))
