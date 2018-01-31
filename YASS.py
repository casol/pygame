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

class Ship(object):
    def __init__(self):
        """The constructor of the class."""
        self.ship_image = pygame.image.load('ship.png')
        # ship start position - middle of screen
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.rotation_step = 3

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

    def draw(self, surface):
        """Draw on surface."""
        # blit yourself at your current position
        surface.blit(self.ship_image, (self.x, self.y))

# create an instance
ship = Ship()


x = 400
y = 300
distance = 10
angle = 10

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
