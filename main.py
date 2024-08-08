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


def flip(sprite):
    return [pygame.transform.flip(frame, True, False) for frame in sprite]


def load_spritesheet(path, width, height, direction=False):
    full_path = path
    images = [f for f in listdir(full_path) if isfile(join(full_path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(full_path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect((i * width, 0, width, height))
            surf.blit(sprite_sheet, (0, 0), rect)

            sprites.append(pygame.transform.scale2x(surf))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_spritesheet("assets/MainCharacters/NinjaFrog", 32, 32, True)

    def __init__(self, x, y, width, height):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None

        self.direction = "left"

        self.frames_index = 0
        self.fall_count = 0

        self.status = "idle"

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

        self.get_state()
        self.animate()

        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

        self.fall_count += 1
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)

        self.input()
        self.move(self.x_vel, self.y_vel)
        self.draw(win)

    def animate(self):
        self.frames_index += 0.5
        self.image = self.SPRITES[self.status][(int(self.frames_index) % len(self.SPRITES[self.status]))]

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    def get_state(self):
        self.status = "idle" + "_" + self.direction
        if self.x_vel != 0:
            self.status = "run" + "_" + self.direction
        if self.y_vel > 0:
            self.status = "fall" + "_" + self.direction



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
