import pygame
from pygame.locals import *
import sys
import random
import math


pygame.init()

# set up the window
WHITE = (255, 255, 255)
(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hello World!')
DRAG = 0.999
ELASTICITY = 0.75
GRAVITY = (math.pi, 0.002)


def add_vectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return angle, length


class Particle:
    """Creates a particle object."""
    def __init__(self, x_y, size):
        self.x, self.y = x_y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 2
        self.speed = 0
        self.angle = math.pi/2

    def display(self):
        """Draws a particle on the screen."""
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)),
                           self.size, self.thickness)

    def move_particle(self):
        """Move particle."""
        (self.angle, self.speed) = add_vectors(self.angle, self.speed, math.pi, 0.002)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= DRAG

    def bounce(self):
        """Bounce particle form the walls."""
        if self.x >= width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= ELASTICITY

        elif self.x <= self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= ELASTICITY

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY


number_of_particle = 10
particles = []

# creating 10 new particles
for n in range(number_of_particle):
    size = random.randint(10, 20)
    x = random.randint(size, width - size)
    y = 20
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
        particle.bounce()
        particle.display()
    pygame.display.update()
