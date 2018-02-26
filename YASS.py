# Yet Another Space Shooter
# https://github.com/casol/pygame

import pygame
import sys
import random
import os

from pygame.locals import *  # pygame.locals.QUIT --> QUIT
vec = pygame.math.Vector2

# game assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sound_folder = os.path.join(game_folder, 'sound')

# initialize pygame
pygame.init()
FPS = 60  # frames per second
fps_clock = pygame.time.Clock()

# drew text
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# set up the window
WIDTH = 1200
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('YESS - Yet_Another_Space_Shooter')

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_SPEED = 7


class Player(pygame.sprite.Sprite):
    """The player's ship."""
    def __init__(self):
        """Initialise player object."""
        # Call the parent class (Sprite constructor)
        pygame.sprite.Sprite.__init__(self)
        # set ship image
        self.original_image = player_img  # image before rotation
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)  # the acceleration vec points upwards
        self.angle_speed = 0
        self.angle = 0
        self.radius = 25  # setting the sprite’s radius

    def update(self):
        """Move based on keys pressed."""
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle_speed = -2.5  # ship rotates counterclockwise
            player.rotate()
        if keys[K_RIGHT]:
            self.angle_speed = 2.5  # ship rotates clockwise
            player.rotate()
        # If up is pressed, accelerate the ship by
        # adding the acceleration to the velocity vector.
        if keys[K_UP]:
            self.vel += self.acceleration
        if keys[K_SPACE]:
            player.shoot()
        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        """Rotate an image while keeping its center."""
        # Rotate the acceleration vector.
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y <= 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self):
        missile = Missile(self.rect.center, self.acceleration, self.angle)
        all_sprites.add(missile)
        missiles.add(missile)


class Missile(pygame.sprite.Sprite):
    """A missile launched by the player's ship."""
    def __init__(self, position, direction, angle):
        """Initialize missile sprite. Take the position,
         direction and angle of the player.
         """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10], pygame.SRCALPHA)
        self.image.fill(BLUE)
        # rotate the image by the player.angle
        self.image = pygame.transform.rotate(self.image, angle)
        # Pass the center of the player as the center of the bullet.rect.
        self.rect = self.image.get_rect(center=position)
        self.position = vec(position)  # The position vector.
        self.velocity = direction * 21  # Multiply by desired speed.

    def update(self):
        """Move the bullet."""
        self.position += self.velocity  # Update the position vector.
        self.rect.center = self.position  # And the rect.

        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Asteroid object."""
    def __init__(self):
        """Initialize asteroid sprite."""
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.80 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-3, 3)

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)



# load all games graphic
background = pygame.image.load(os.path.join(img_folder, 'darkPurple.png')).convert()
background_rect = background.get_rect()

background = pygame.transform.scale(background, (1200, 800))
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()

meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
               'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
missiles = pygame.sprite.Group()

player = Player()
#all_sprites.add(player)

for i in range(8):
    d = Asteroid()
    all_sprites.add(d)
    asteroids.add(d)
# player score
score = 0


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
    draw_text(DISPLAY, str(score), 18, WIDTH / 2, 10)
    player.draw(DISPLAY)
    player.update()
    player.wrap_around_screen()

    # check if a missile hit an asteroid
    hits = pygame.sprite.groupcollide(asteroids, missiles, True, True)
    # create new
    for hit in hits:
        score += 50
        d = Asteroid()
        all_sprites.add(d)
        asteroids.add(d)

    # see if the player Sprite has collided with anything in the asteroids Group
    hits = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_circle)
    if hits:
        pass
        #pygame.quit()
        #sys.exit()

    #txt = FONT.render('angle {:.1f}'.format(player.angle), True, (150, 150, 170))
    #DISPLAY.blit(txt, (10, 10))
    pygame.display.update()
    fps_clock.tick(FPS)
