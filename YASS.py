# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
import random
import os
import math
from pygame.locals import *  # pygame.locals.QUIT --> QUIT

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
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    """The player's ship."""
    def __init__(self):
        """Initialise player object."""
        # Call the parent class (Sprite constructor)
        pygame.sprite.Sprite.__init__(self)
        # set ship image
        self.original_image = player_img  # image before rotation
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.delta_x = 1
        self.delta_y = 1
        self.rotation = 0
        self.rotation_speed = 3
        self.rotation_speed_r = -3
        self.velocity_step = 2

    def update(self):
        """Move based on keys pressed."""
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:  # ship rotates clockwise
            self.rotate_r()
        elif key[K_LEFT]:  # ship rotates counterclockwise.
            self.rotate()
        if key[K_SPACE]:
            player.shoot()

    def rotate(self):
        """Rotate an image while keeping its center."""
        self.rotation = (self.rotation + self.rotation_speed) % 360
        new_image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center  # save its current center
        self.image = new_image
        self.rect = self.image.get_rect()  # replace old rect with new rect
        self.rect.center = old_center  # put the new rect's center at old center

    def rotate_r(self):
        """Rotate an image while keeping its center."""
        self.rotation = (self.rotation + self.rotation_speed_r) % 360
        new_image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center  # save its current center
        self.image = new_image
        self.rect = self.image.get_rect()  # replace old rect with new rect
        self.rect.center = old_center  # put the new rect's center at old center

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom <= 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self):
        missile = Missile(self.rect.centerx, self.rect.top)
        all_sprites.add(missile)
        missiles.add(missile)


class Missile(pygame.sprite.Sprite):
    """A missile launched by the player's ship."""
    def __init__(self, x, y):
        """Initialize missile sprite."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        # missile going upward
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # out of the screen
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Asteroid object."""
    def __init__(self):
        """Initialize asteroid sprite."""
        pygame.sprite.Sprite.__init__(self)
        self.image = asto_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.80 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


# load all games graphic
background = pygame.image.load(os.path.join(img_folder, 'darkPurple.png')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, (800, 800))
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()
asto_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_med1.png')).convert()


all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
missiles = pygame.sprite.Group()

player = Player()
#all_sprites.add(player)

for i in range(8):
    d = Asteroid()
    all_sprites.add(d)
    asteroids.add(d)


while True:  # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BLACK)
    DISPLAY.blit(background, background_rect)
    # drew / update
    all_sprites.update()
    all_sprites.draw(DISPLAY)
    player.draw(DISPLAY)
    player.update()
    player.wrap_around_screen()
    # check if a missile hit an asteroid
    hits = pygame.sprite.groupcollide(asteroids, missiles, True, True)
    # create new
    for hit in hits:
        d = Asteroid()
        all_sprites.add(d)
        asteroids.add(d)

    # see if the player Sprite has collided with anything in the asteroids Group
    hits = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_circle)
    if hits:
        pass
        # pygame.quit()
        # sys.exit()

    print('top:', player.rect.top, 'bottom:', player.rect.bottom,
          'rect_x:', player.rect.x, 'rect_y:', player.rect.y,
          player.rotation, player.rect.center)

    pygame.display.update()
    fps_clock.tick(FPS)
