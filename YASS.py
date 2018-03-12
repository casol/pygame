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

MAX_SPEED = 6


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
        self.previous_time = pygame.time.get_ticks()
        self.missile_delay = 500  # how long the ship should wait before shooting
        self.health = 100  # player health bar

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
            # delay missile
            current_time = pygame.time.get_ticks()
            if current_time - self.previous_time > self.missile_delay:  # subtract the time since the last tick
                self.previous_time = current_time
                # fire when 500 ms have passed
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
        # create and add the missile object to the group
        missile = Missile(self.rect.center,
                          self.vel + 40 * self.acceleration,
                          player.acceleration.as_polar()[1])
        all_sprites.add(missile)
        missiles.add(missile)

    def drew_health_bar(self, surface, x, y, health):
        """Draw health bar."""
        if health < 0:
            health = 0
        bar_length = 100
        bar_height = 10
        fill = (health / 100) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)


class Missile(pygame.sprite.Sprite):
    """This class represents the bullet.
     A missile launched by the player's ship.
     """

    def __init__(self, position, velocity, angle):
        """Initialize missile sprite.
         Take the velocity, direction and angle of the player.
         """
        pygame.sprite.Sprite.__init__(self)
        self.original_image = missile_img  # image before rotation
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        # Rotate the image by the player.angle
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        self.image.set_colorkey(BLACK)
        # Pass the center of the player as the center of the bullet.rect
        self.rect = self.image.get_rect(center=position)
        self.position = vec(position)  # The position vector
        self.velocity = velocity

    def update(self):
        """Move the bullet."""
        self.position += self.velocity  # Update the position vector
        self.rect.center = self.position  # And the rect
        # Kill when the projectile leaves the screen
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
        """Rotate an asteroid image while keeping its center."""
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


class Explosion(pygame.sprite.Sprite):
    """Explosion object."""
    def __init__(self, center, size):
        """Initialize explosion sprite."""
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 8

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all games graphic
background = pygame.image.load(os.path.join(img_folder, 'darkPurple.png')).convert()
background_rect = background.get_rect()

background = pygame.transform.scale(background, (1200, 800))
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()
missile_img = pygame.image.load(os.path.join(img_folder, 'laserGreen05.png')).convert()
# Asteroids graphic
img_folder_meteors = os.path.join(img_folder, 'meteors')
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
               'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder_meteors, img)).convert())

# Explosion
img_folder_explosions = os.path.join(img_folder, 'explosion_animations')
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['mid'] = []
explosion_anim['sm'] = []

for i in range(1, 65):
    image_name = '{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder_explosions, image_name)).convert()
    img.set_colorkey(BLACK)
    #img_lg = pygame.transform.scale(img, (100, 100))
    explosion_anim['lg'].append(img)

    img_mid = pygame.transform.scale(img, (93, 93))
    explosion_anim['mid'].append(img_mid)

    img_sm = pygame.transform.scale(img, (50, 50))
    explosion_anim['sm'].append(img_sm)


all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
missiles = pygame.sprite.Group()

player = Player()
#all_sprites.add(player)


def new_asteroid():
    new_asd = Asteroid()
    all_sprites.add(new_asd)
    asteroids.add(new_asd)

# create asteroids
for i in range(8):
    new_asteroid()

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
    player.drew_health_bar(DISPLAY, 10, 10, player.health)

    # Find all sprites that collide between two groups
    # check if a missile hit an asteroid
    missile_hits = pygame.sprite.groupcollide(asteroids, missiles, True, True)
    # Check the list of colliding sprites
    for hit in missile_hits:
        score += 50 - hit.radius  # assign points based on the size of asteroid
        print(hit.radius)
        # animate explosion based on the size of asteroid
        if hit.radius > 34:
            explosion = Explosion(hit.rect.center, 'lg')
        else:
            explosion = Explosion(hit.rect.center, 'mid')
        all_sprites.add(explosion)
        new_asteroid()  # spawn a new asteroid

    # See if the player Sprite has collided with anything in the asteroids Group
    # The True flag will remove the sprite in asteroids group
    # Return a list containing all Sprites in a Group that intersect with another Sprite
    hits = pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_asteroid()  # spawn a new asteroid
        if player.health <= 0:
            pass
            pygame.quit()
            sys.exit()

    #txt = FONT.render('angle {:.1f}'.format(player.angle), True, (150, 150, 170))
    #DISPLAY.blit(txt, (10, 10))
    pygame.display.update()
    fps_clock.tick(FPS)
