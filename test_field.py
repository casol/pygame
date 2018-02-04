""" rotate.py
    demonstrate rotating a sprite"""

import pygame
import os

pygame.init()


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("ship.png")
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.dir = 0

    def update(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def turnLeft(self):
        self.dir += 5
        if self.dir > 360:
            self.dir = 45

    def turnRight(self):
        self.dir -= 5
        if self.dir < 0:
            self.dir = 315


def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Rotate a sprite")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    ship = Ship()
    allSprites = pygame.sprite.Group(ship)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.turnLeft()
                elif event.key == pygame.K_RIGHT:
                    ship.turnRight()

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
