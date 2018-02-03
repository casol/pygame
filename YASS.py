# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
import random
import os
from pygame.locals import *  # pygame.locals.QUIT --> QUIT

# game assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sound_folder = os.path.join(game_folder, 'sound')
player_img = pygame.image.load(os.path.join(img_folder, 'ship.png'))

# initialize pygame
pygame.init()

FPS = 60  # frames per second
fps_clock = pygame.time.Clock()

# set up the window
WIDTH = 800
HEIGHT = 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    """Create sprite."""
    def __init__(self):
        # Call the parent class (Sprite constructor)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speed_x = 0
        self.speed_y = 0
        self.x = 0
        self.y = 0

    def update(self):
        """Rotate based on keys pressed."""
        key = pygame.key.get_pressed()
        distance = 5  # distance moved in 1 frame
        if key[K_DOWN]:  # down key
            self.rect.y += distance  # move down
        elif key[K_UP]:  # up key
            self.rect.y -= distance  # move up
        if key[K_RIGHT]:  # right key
            self.rect.x += distance  # move right
        elif key[K_LEFT]:  # left key
            self.rect.x -= distance  # move left

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while True:  # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BLACK)
    # drew / update
    all_sprites.update()
    all_sprites.draw(DISPLAY)
    pygame.display.update()
    fps_clock.tick(FPS)
