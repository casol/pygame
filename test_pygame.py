import pygame
from pygame.locals import *
import sys
import random
import math


pygame.init()

# set up the window
WHITE = (255, 255, 255)
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hello World!')


# object
class Particle:
    """Creates a particle object."""
    def __init__(self, x_y, size):
        self.x, self.y = x_y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 2
        self.speed = 0.01
        self.angle = math.pi/2

    def display(self):
        """Draws a particle on the screen."""
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)),
                           self.size, self.thickness)

    def move_particle(self):
        """ """
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed


number_of_particle = 10
particles = []

# creating 10 new particles
for n in range(number_of_particle):
    size = random.randint(10, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    particle = (Particle((x, y), size))
    # update speed and angle of existing object
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)
    # add new particle to the list
    particles.append(particle)

while True:  # main loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # remove old drawing by filling screen with background color
    screen.fill(WHITE)

    for particle in particles:
        particle.move_particle()
        particle.display()
    pygame.display.update()
