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
        self.image = player_img
        # resize original ship image
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.delta_x = 0
        self.delta_y = 0

    def update(self):
        """Move based on keys pressed."""
        self.delta_x = 5
        self.delta_y = 5
        key = pygame.key.get_pressed()
        if key[K_DOWN]:  # down key
            self.rect.y += self.delta_y  # move down
        elif key[K_UP]:  # up key
            self.rect.y -= self.delta_y  # move up
        if key[K_RIGHT]:  # right key
            self.rect.x += self.delta_x  # move right
        elif key[K_LEFT]:  # left key
            self.rect.x -= self.delta_x  # move left
        if key[K_SPACE]:
            player.shoot()

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

    # check if a asteroid the the ship
    hits = pygame.sprite.spritecollide(player, asteroids, False)
    if hits:
        pygame.quit()
        sys.exit()

    print(player.rect.x, player.rect.y, 'top:', player.rect.top, 'bottom:', player.rect.bottom,
          'rect_x:', player.rect.x, 'rect_y:', player.rect.y, player.rect.centerx)

    pygame.display.update()
    fps_clock.tick(FPS)
