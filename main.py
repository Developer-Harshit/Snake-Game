# Snake Game
# Snake Ganan

import pygame
from random import randint, random, choice
from scripts.utils import DemoObject, load_image, load_images
from scripts.tilemap import Tilemap
from scripts.entity import Player
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
        self.assets = {
            "ground": load_images("ground", (size, size)),
            "wall": load_images("wall", (size, size)),
            "player": load_image("player.png", (size, size)),
            "tail": load_image("tail.png", (size, size)),
        }

        # --------------------------------------------------------------------------

        self.tilemap = Tilemap(self)
        self.tilemap.create_random(WIDTH * 2, HEIGHT * 2)

        self.player = Player(self)
        self.scroll = [0, 0]

        # --------------------------------------------------------------------------

    def run(self):
        running = True
        frame = 0
        while running:
            # Handling scroll -----------------------------------------------------|
            # self.scoll[0] += 1 / self.size

            # self.scoll[1] += 1 / self.size
            # For Camera ----------------------------------------------------------|
            p_pos = self.player.block.get_rect().center
            self.scroll[0] += (
                p_pos[0] - self.display.get_width() / 2 - self.scroll[0]
            ) / self.size
            self.scroll[1] += (
                p_pos[1] - self.display.get_height() / 2 - self.scroll[1]
            ) / self.size
            # THats why we are converting it into int
            render_scroll = ((self.scroll[0]), (self.scroll[1]))

            # For Background ------------------------------------------------------|

            self.display.fill(BG_COLOR)

            self.tilemap.render(self.display, render_scroll)

            self.display.blit(self.bg_layer, (0, 0))
            # For Player ----------------------------------------------------------|
            if frame % 12 == 0:
                self.player.update()
            self.player.render(self.display, render_scroll)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    if event.key == pygame.K_SPACE:
                        self.player.add_tail()

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
            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            frame += 1

    def quit(self):
        # Quit --------------------------------------------------------------------|
        pygame.quit()
        sys.exit()
        exit()


if __name__ == "__main__":
    Game().run()
print("Game Over")
