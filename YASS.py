# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
import random
import os
import math
from pygame.locals import *  # pygame.locals.QUIT --> QUIT
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
WIDTH = 1200
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_SPEED = 9


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
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)  # the acceleration vec points upwards
        self.angle_speed = 0
        self.angle = 0
        self.radius = 25  # setting the sprite’s radius
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """Move based on keys pressed."""
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle_speed = -2.5  # ship rotates counterclockwise
            player.rotate()
        if keys[K_RIGHT]:
            self.angle_speed = 2.5  # ship rotates clockwise
            player.rotate()
        # If up or down is pressed, accelerate the ship by
        # adding the acceleration to the velocity vector.
        if keys[K_UP]:
            self.vel += self.acceleration
        if keys[K_SPACE]:
            player.shoot()
        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        """Rotate an image while keeping its center."""
        # Rotate the acceleration vector.
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.acceleration.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            if self.angle > 360:
                self.angle -= 360
            elif self.angle < 0:
                self.angle += 360
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y <= 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0

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
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
background = pygame.transform.scale(background, (1200, 800))
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
        #pygame.quit()
        #sys.exit()

    pygame.display.update()
    fps_clock.tick(FPS)
