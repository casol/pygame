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
pygame.display.set_caption('TEST -> MOVING AND ROTATION')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set ship image
        self.original_image = player_img  # image before rotation
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # movement
        self.angle = math.pi / 2
        self.angle_change = 0
        self.trajectory_angle = self.angle

        self.speed = 0
        self.thrust = 0
        self.max_speed = 12

    def drew(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw_spaceship(self, screen):
        magnitude = 30
        p1_angle = self.angle
        p2_angle = self.angle + math.radians(145)
        p3_angle = self.angle - math.radians(145)
        p1 = (math.cos(p1_angle) * magnitude + self.rect.x, -math.sin(p1_angle) * magnitude + self.rect.y)
        p2 = (math.cos(p2_angle) * magnitude + self.rect.x, -math.sin(p2_angle) * magnitude + self.rect.y)
        p3 = (math.cos(p3_angle) * magnitude + self.rect.x, -math.sin(p3_angle) * magnitude + self.rect.y)

        pygame.draw.line(screen, WHITE, (p1[0], p1[1]), (p2[0], p2[1]))
        pygame.draw.line(screen, WHITE, (p1[0], p1[1]), (p3[0], p3[1]))
        pygame.draw.line(screen, WHITE, (p2[0], p2[1]), (p3[0], p3[1]))
        pygame.draw.circle(screen, RED, (int(self.rect.x), int(self.rect.y)), 1)

    def add_vectors(self):
        x = math.sin(self.trajectory_angle) * self.speed + math.sin(self.angle) * self.thrust
        y = math.cos(self.trajectory_angle) * self.speed + math.cos(self.angle) * self.thrust
        # pi/2 -> 90°
        self.trajectory_angle = 0.5 * math.pi - math.atan2(y, x)
        self.speed = math.hypot(x, y)

    def position(self):
        self.rect.x += math.cos(self.trajectory_angle) * self.speed
        self.rect.y -= math.sin(self.trajectory_angle) * self.speed

    def update(self):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                #self.angle_change = .03
                self.angle += .03
            elif event.key == K_RIGHT:
                #self.angle_change = -.03
                self.angle += -.03
            elif event.key == K_UP:
                self.thrust = .04

        if event.type == KEYUP:
            if event.key == K_LEFT:
                self.angle_change = 0
            elif event.key == K_RIGHT:
                self.angle_change = 0
            elif event.key == K_UP:
                self.thrust = 0

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

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()

player = Player()


while True:  # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAY.fill(BLACK)

    player.update()
    player.position()
    player.add_vectors()
    player.draw_spaceship(DISPLAY)
    player.wrap_around_screen()

    print('x:', player.rect.x, 'y:', player.rect.y, 'player.angle:', player.angle)
    print('trajectory_ang:', player.trajectory_angle, 'speed:', player.speed, 'thrust:', player.thrust)
    pygame.display.update()
    fps_clock.tick(FPS)
