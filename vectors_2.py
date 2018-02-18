# vectors
import pygame
import sys
import random
import os
import math
from pygame.locals import *  # pygame.locals.QUIT --> QUIT
# Vector2
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
WIDTH = 800
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('VECTOR_2')
FONT = pygame.font.Font(None, 24)

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_SPEED = 9


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set ship image
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (50, 120, 180), ((35, 0), (0, 35), (70, 35)))
        #self.original_image = player_img  # image before rotation
        #self.image = self.original_image
        #self.image = pygame.Surface((40, 40))
        #self.image.fill(GREEN)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # position
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # velocity
        self.vel = vec(0, 0)
        # acceleration
        self.acc = vec(0, 0)
        # heading vector
        self.heading = vec(0, -1)  # The vector points upwards
        self.rect.center = self.pos

        self.angle_speed = 0
        self.angle = 0

    def update(self):
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.acc.x = -0.2
        if keys[K_RIGHT]:
            self.acc.x = 0.2

        if keys[K_UP]:
            self.acc.y = -0.2

        if keys[K_DOWN]:
            self.acc.y = 0.2

        if keys[K_a]:
            self.angle_speed = -1
            player.rotate()
        if keys[K_d]:
            self.angle_speed = 1
            player.rotate()

        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        # angle to radians
        rad = math.radians(self.angle)

        self.vel += self.acc
        self.pos += self.vel

        #self.vel.x += self.acc.x * math.sin(rad)
        #self.vel.y += self.acc.y * -math.cos(rad)

        self.rect.center = self.pos

    def rotate(self):
        # Rotate the heading vector and then the image
        self.heading.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_vectors(self, screen):
        scale = 20
        # vel
        pygame.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pygame.draw.line(screen, RED, self.pos, (self.pos + self.heading * scale), 5)

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y <= 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while True:  # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BLACK)
    player.wrap_around_screen()
    all_sprites.update()
    all_sprites.draw(DISPLAY)
    player.draw_vectors(DISPLAY)

    txt = FONT.render('heading angle {:.1f}'.format(player.angle), True, (150, 150, 170))
    DISPLAY.blit(txt, (10, 10))

    pygame.display.update()
    fps_clock.tick(FPS)
    print('vel:', player.vel, player.acc, player.heading)
