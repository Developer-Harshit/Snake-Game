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

        size = 16
        self.size = size
        self.assets = {
            "tiles": load_images("tiles", (size, size)),
            "head": load_image("head.png", (size, size)),
        }

        # --------------------------------------------------------------------------

        self.tilemap = Tilemap(self)
        self.tilemap.create_random(WIDTH, HEIGHT)

        self.player = Player(self)
        # --------------------------------------------------------------------------

    def run(self):
        running = True
        frame = 0
        while running:
            # For Background ------------------------------------------------------|

            self.display.fill(BG_COLOR)

            self.tilemap.render(self.display)
            if frame % 10 == 0:
                self.player.update()
            self.player.render(self.display)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
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
