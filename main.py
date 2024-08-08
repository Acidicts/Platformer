import os
import sys
import math
import pygame
import random
from os import listdir
from os.path import isfile, join


pygame.init()

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_VEL = 5

pygame.display.set_caption("Platformer")
surf = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None

        self.direction = "left"

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def input(self):
        keys = pygame.key.get_pressed()

        self.x_vel = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * PLAYER_VEL

        if self.x_vel != 0:
            self.direction = "right" if self.x_vel > 0 else "left"

    def update(self, fps):
        win = pygame.display.get_surface()
        self.input()
        self.move(self.x_vel, self.y_vel)
        self.draw(win)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, w, h = image.get_rect()
    tiles = []

    for i in range(int(WIDTH // w + 1)):
        for j in range(int(HEIGHT // h + 1)):
            pos = [i * w, j * h]
            tiles.append(pos)

    return tiles, image


def draw(surf, background, bg_image):
    for tile in background:
        surf.blit(bg_image, tile)

    player.update(60)

    pygame.display.update()


def main(win):
    clock = pygame.time.Clock()
    background = get_background("Blue.png")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw(win, background[0], background[1])

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    player = Player(50, 50, 50, 50)
    main(surf)
