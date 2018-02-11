# vectors
import pygame
import sys
import random
import os
import math
from pygame.locals import *  # pygame.locals.QUIT --> QUIT
# Vector2
vec = pygame.math.Vector2

# game assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sound_folder = os.path.join(game_folder, 'sound')

# initialize pygame
pygame.init()

FPS = 60  # frames per second
fps_clock = pygame.time.Clock()

# set up the window
WIDTH = 800
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('VECTOR_2')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set ship image
        # self.original_image = player_img  # image before rotation
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # velocity
        self.vel = vec(0, 0)
        # acceleration
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.acc.x = -0.2
        if keys[K_RIGHT]:
            self.acc.x = 0.2

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.acc.y = -0.2
        if keys[K_DOWN]:
            self.acc.y = 0.2

        self.vel += self.acc
        # max speed

        if self.vel[1] > 9:
            self.vel[1] = 9
        elif self.vel[1] < -9:
            self.vel[1] = -9

        if self.vel[0] > 9:
            self.vel[0] = 9
        elif self.vel[0] < -9:
            self.vel[0] = -9


        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y <= 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while True:  # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BLACK)
    player.wrap_around_screen()
    all_sprites.update()
    all_sprites.draw(DISPLAY)
    pygame.display.update()
    fps_clock.tick(FPS)
    print(player.vel)
