from random import random, choice, randint
from scripts.utils import load_image, load_images
from perlin_noise import PerlinNoise
import pygame
import json

COLLISION_TILES = ["wall"]

NEIGHBOR_OFFSET = [(0, -1), (-1, 0), (0, 1), (1, 0)]


def loc_to_str(x, y):
    return str(x) + ";" + str(y)


class Tile:
    def __init__(self, pos, t_type, variant):
        self.pos = tuple(pos)
        self.type = t_type
        self.variant = variant

        # for A-Star
        self.g, self.h, self.f = 10**10, 0, 0

    def get_object(self):
        return {"pos": self.pos, "type": self.type, "variant": self.variant}

    def gCost(self, other):
        self.g = other.g + 1
        return self.g

    def heuristics(self, goal):
        self.h = abs(self.pos[0] - goal.pos[0]) + abs(self.pos[1] - goal.pos[1])
        return self.h

    def get_neighbours(self, nodemap):
        result = []
        for offset in NEIGHBOR_OFFSET:
            neighbour_loc = (
                str(self.pos[0] + offset[0]) + ";" + str(self.pos[1] + offset[1])
            )
            if neighbour_loc in nodemap:
                result.append(nodemap[neighbour_loc])
        return result


class Tilemap:
    def __init__(self, game, map={}):
        self.game = game
        self.map = map
        
    def reset_cost(self):
        for tile in self.map.values():
            tile.g, tile.h, tile.f = 10**10, 0, 0

    def save(self, file_name):
        my_map = {}
        for loc in self.map:
            my_tile = self.map[loc]
            my_map[loc] = my_tile.get_object()

        f = open("assets/maps/" + file_name, "w")
        json.dump({"map": my_map, "size": self.game.size}, f)
        f.close()

    def load(self, file_name):
        f = open("assets/maps/" + file_name, "r")
        data = json.load(f)
        f.close()
        self.map = {}
        for loc in data["map"]:
            tile_obj = data["map"][loc]
            self.map[loc] = Tile(tile_obj["pos"], tile_obj["type"], tile_obj["variant"])
        self.game.size = data["size"]

    def get_global_pos(self, loc, offset=(0, 0)):
        return (
            loc[0] * self.game.size - offset[0],
            loc[1] * self.game.size - offset[1],
        )

    def copy(self):
        return Tilemap(self.game, self.map)

    def get_collision_pos(self):
        result = []
        for tile in self.map.values():
            if tile.type in COLLISION_TILES:
                result.append(tile.pos)
        return result

    def render(self, surf, offset=[0, 0]):
        for tile in self.map.values():
            pos = self.get_global_pos(tile.pos, offset)

            surf.blit(self.game.assets[tile.type][tile.variant], pos)
