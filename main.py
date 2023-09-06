# Snake Game
# Snake Ganan


import cProfile
import pstats

import pygame
from random import randint, random, choice
from scripts.utils import DemoObject, load_image, load_images, lerp
from scripts.tilemap import Tilemap
from scripts.entity import Player, Enemy
import sys

print("Starting Game")

from scripts.const import WIDTH, HEIGHT, BG_COLOR, BLUE, RED


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)

        self.display = self.screen.copy()

        self.clock = pygame.time.Clock()

        self.bg_layer = self.display.copy()
        self.bg_layer.fill((11, 1, 31))
        self.bg_layer.set_alpha(150)

        size = 32
        self.size = size
        self.reload_assets()

        # --------------------------------------------------------------------------

        self.tilemap = Tilemap(self)
        self.tilemap.load("test.json")

        self.player = Player(self, (2, 2))
        self.enemy = Enemy(self, "archer", (6, 6))

        self.scroll = [0, 0]

        # --------------------------------------------------------------------------

    def resize(self):
        if self.display.get_size() == self.screen.get_size():
            return
        self.display = pygame.surface.Surface(self.screen.get_size())
        self.bg_layer = self.display.copy()
        self.bg_layer.fill((11, 1, 31))
        self.bg_layer.set_alpha(150)

    def reload_assets(self):
        size = self.size
        self.assets = {
            "ground": load_images("ground", (size, size)),
            "wall": load_images("wall", (size, size)),
            "player/head": load_image("player/head.png", (size, size)),
            "player/tail": load_image("player/tail.png", (size, size)),
            "enemy/head": load_image("enemy/head.png", (size, size)),
            "enemy/tail": load_image("enemy/tail.png", (size, size)),
            "archer/head": load_image("archer/head.png", (size, size)),
            "archer/tail": load_image("archer/tail.png", (size, size)),
        }

    def run(self):
        running = True
        frame = 0
        while running:
            # Handling scroll ------------------------------------------------------------------------------|

            p_pos = self.player.get_rect().center

            # Lerping to get smooth scroll a+=(b - a) * t
            self.scroll[0] += (
                p_pos[0] - self.display.get_width() / 2 - self.scroll[0]
            ) / (self.size)
            self.scroll[1] += (
                p_pos[1] - self.display.get_height() / 2 - self.scroll[1]
            ) / (self.size)

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            # ----------------------------------------------------------------------------------------------|
            # Collision_Blocks -----------------------------------------------------------------------------|
            self.collide_pos = []
            for block in self.player.tail.tail:
                if block.pos == self.player.pos:
                    continue
                self.collide_pos.append(tuple(block.pos))

            for block in self.enemy.tail.tail:
                if block.pos == self.enemy.pos:
                    continue
                self.collide_pos.append(tuple(block.pos))

            # For Background -------------------------------------------------------------------------------|

            self.display.fill(BG_COLOR)

            self.tilemap.render(self.display, render_scroll)

            self.display.blit(self.bg_layer, (0, 0))
            # ----------------------------------------------------------------------------------------------|

            # For Player -----------------------------------------------------------------------------------|
            self.player.update(frame)

            self.player.render(self.display, render_scroll)
            if self.player.death > 0:
                self.player = Player(self, (2, 2))

            # ----------------------------------------------------------------------------------------------|

            # For Enemy ------------------------------------------------------------------------------------|
            self.enemy.update(frame)

            self.enemy.render(self.display, render_scroll)
            if self.enemy.death > 0:
                self.enemy = Enemy(self, "archer", (2, 2))
            # ----------------------------------------------------------------------------------------------|

            # Checking Events ------------------------------------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    # self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        # self.quit()
                    if event.key == pygame.K_SPACE:
                        self.player.tail.count += 1
                        pass
                    if event.key == pygame.K_w:
                        self.player.change_direction((0, -1))
                    if event.key == pygame.K_a:
                        self.player.change_direction((-1, 0))
                    if event.key == pygame.K_s:
                        self.player.change_direction((0, 1))
                    if event.key == pygame.K_d:
                        self.player.change_direction((1, 0))

                    pass
                if event.type == pygame.KEYUP:
                    pass
            # ----------------------------------------------------------------------------------------------|

            # Bliting in screen ----------------------------------------------------------------------------|
            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            self.resize()
            frame += 1
            # ----------------------------------------------------------------------------------------------|

    def quit(self):
        pygame.quit()
        sys.exit()
        exit()


if __name__ == "__main__":
    with cProfile.Profile() as profile:
        Game().run()
    result = pstats.Stats(profile)
    # result.sort_stats(pstats.SortKey.TIME)
    # result.dump_stats("prof/result.prof")
print("Game Over")
