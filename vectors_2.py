import sys
import pygame
from pygame.locals import *
vec = pygame.math.Vector2

pygame.init()
FPS = 60
fps_clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
previous_time = pygame.time.get_ticks()

MAX_SPEED = 7


class Player(pygame.sprite.Sprite):
    """This class represents the Player."""

    def __init__(self):
        """Set up the player on creation."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (50, 120, 180), ((35, 0), (0, 35), (70, 35)))
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)  # The acceleration vec points upwards.
        self.angle_speed = 0
        self.angle = 0
        self.previous_time = pygame.time.get_ticks()  # Store the previous time when a bullet was fired

    def update(self):
        """Update the player's position."""
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle_speed = -2
            player.rotate()
        if keys[K_RIGHT]:
            self.angle_speed = 2
            player.rotate()
        # If up is pressed, accelerate the ship by
        # adding the acceleration to the velocity vector.
        if keys[K_UP]:
            self.vel += self.acceleration
        if keys[K_SPACE]:
            # delay missile
            current_time = pygame.time.get_ticks()
            if current_time - self.previous_time > 500:  # subtract the time since the last tick
                self.previous_time = current_time
                # fire when 500 ms have passed
                player.shoot()

        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        # rotate the acceleration vector
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

    def shoot(self):
        # create and add missile object to the group
        missile = Missile(self.rect.center,
                          self.vel + 40 * self.acceleration,  # new value here!
                          player.acceleration.as_polar()[1])
        all_sprites.add(missile)
        missiles.add(missile)
        print(missile.velocity)


class Missile(pygame.sprite.Sprite):
    """This class represents the bullet.
     A missile launched by the player's ship.
     """

    def __init__(self, position, velocity, angle):
        """Initialize missile sprite.
         Take the position, direction and angle of the player.
         """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10], pygame.SRCALPHA)
        self.image.fill(BLUE)
        # Rotate the image by the player.angle
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        # Pass the center of the player as the center of the bullet.rect.
        self.rect = self.image.get_rect(center=position)
        self.position = vec(position)  # The position vector.
        self.velocity = velocity

    def update(self):
        """Move the bullet."""
        self.position += self.velocity  # Update the position vector.
        self.rect.center = self.position  # And the rect.

        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
missiles = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    player.wrap_around_screen()
    all_sprites.update()

    DISPLAY.fill(BLACK)
    all_sprites.draw(DISPLAY)
    pygame.display.set_caption('angle {:.1f} accel {} accel angle {:.1f}'.format(
        player.angle, player.acceleration, player.acceleration.as_polar()[1]))
    pygame.display.update()
    fps_clock.tick(FPS)
