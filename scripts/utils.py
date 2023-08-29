import pygame
import os
from scripts.const import BASE_IMG_PATH


def load_image(rpath, scale=False, alpha=255):
    path = BASE_IMG_PATH + rpath

    img = pygame.image.load(path).convert()  # convert method makes it easier to render

    img.set_colorkey((0, 0, 0))
    img.set_alpha(alpha)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


def load_images(path, scale=False):
    images = []
    for img_path in os.listdir(BASE_IMG_PATH + path):
        img = load_image(path + "/" + img_path, scale)

        images.append(img)
    return images


def add_vector(one, two):
    return (one[0] + two[0], one[1] + two[1])


class DemoObject:
    def __init__(self, pos, spirite):
        self.pos = list(pos)
        self.sprite = spirite

    def render(self, surf):
        surf.blit(self.sprite, self.pos)
