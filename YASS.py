# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
from pygame.locals import *  # pygame.locals.QUIT --> QUIT

pygame.init()

FPS = 30  # frames per second
fps_clock = pygame.time.Clock()

# set up the window
DISPLAY = pygame.display.set_mode((800, 600))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')
# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class Ship(object):
    def __init__(self):
        """The constructor of the class."""
        self.ship_image = pygame.image.load('ship.png')
        # ship start position
        self.x = 100
        self.y = 100

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        distance = 5  # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]:  # down key
            self.y += distance  # move down
        elif key[pygame.K_UP]:  # up key
            self.y -= distance  # move up
        if key[pygame.K_RIGHT]:  # right key
            self.x += distance  # move right
        elif key[pygame.K_LEFT]:  # left key
            self.x -= distance  # move left

    def draw(self, surface):
        """Draw on surface."""
        # blit yourself at your current position
        surface.blit(self.ship_image, (self.x, self.y))

# create an instance
ship = Ship()

while True:  # game loop
    DISPLAY.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    ship.handle_keys()
    ship.draw(DISPLAY)
    pygame.display.update()
    fps_clock.tick(FPS)
