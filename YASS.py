# Yet Another Space Shooter
import pygame
import sys
from pygame.locals import *  # pygame.locals.QUIT --> QUIT

pygame.init()

FPS = 30  # frames per second
fpsClock = pygame.time.Clock()

# set up the window
DISPLAY = pygame.display.set_mode((800, 600))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')

WHITE = (255, 255, 255)
ship_img = pygame.image.load('ship.png')
shipx = 100
shipy = 100

while True:  # game loop
    DISPLAY.fill(WHITE)
    DISPLAY.blit(ship_img, (shipx, shipy))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
