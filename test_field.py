# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
from pygame.locals import *  # pygame.locals.QUIT --> QUIT

pygame.init()

FPS = 30  # frames per second
fps_clock = pygame.time.Clock()

# set up the window
WIDTH = 800
HEIGHT = 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')
# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

x = 200
y = 300
distance = 5
angle = 10


# subclassing the Sprite
class Block(pygame.sprite.Sprite):
    """Create sprite."""
    def __init__(self, color, width, height, x, y):
        # Call the parent class (Sprite constructor)
        super(Block, self).__init__()
        #pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def draw(self, surface):
        """Draw on surface."""
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


class Ship(pygame.sprite.Sprite):
    """Create ship sprite."""
    def __init__(self):
        # Call the parent class (Sprite constructor)
        pygame.sprite.Sprite.__init__(self)
        self.x = WIDTH/2
        self.y = HEIGHT/2
        # Create an image of the ship
        self.ship_image = pygame.image.load('ship.png')
        self.rect = self.ship_image.get_rect()

    def draw(self, surface):
        """Draw on surface."""
        # blit yourself at your current position
        surface.blit(self.ship_image, (self.x, self.y))

    def handle_keys(self):
        """Rotate based on keys pressed."""
        key = pygame.key.get_pressed()
        distance = 5  # distance moved in 1 frame
        if key[K_DOWN]:  # down key
            self.y += distance  # move down
        elif key[K_UP]:  # up key
            self.y -= distance  # move up
        if key[K_RIGHT]:  # right key
            self.x += distance  # move right
        elif key[K_LEFT]:  # left key
            self.x -= distance  # move left

# block group
block_obj = Block(RED, 20, 30, 600, 500)
blocks = pygame.sprite.Group()
blocks.add(block_obj)


# player group
ship_obj = Ship()
player_group = pygame.sprite.Group()
player_group.add(ship_obj)


while True:  # game loop
    DISPLAY.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # meteor_image = pygame.image.load('meteor.png')
    ship_obj.handle_keys()
    ship_obj.draw(DISPLAY)
    block_obj.draw(DISPLAY)
    pygame.display.update()
    fps_clock.tick(FPS)
