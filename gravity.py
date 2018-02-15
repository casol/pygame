import math
import pygame
from pygame.math import Vector2


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos=(420, 420)):
        super(Player, self).__init__()
        self.image = pygame.Surface([20, 40], pygame.SRCALPHA)
        self.image.fill(RED)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        # The vector points upwards.
        self.direction = Vector2(0, -1)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, pos, direction, angle):
        """Take the pos, direction and angle of the player."""
        super(Bullet, self).__init__()
        self.image = pygame.Surface([4, 10], pygame.SRCALPHA)
        self.image.fill(BLACK)
        # Rotate the image by the player.angle (negative since y-axis is flipped).
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        # Pass the center of the player as the center of the bullet.rect.
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)  # The position vector.
        self.velocity = direction * 11  # Multiply by desired speed.

    def update(self):
        """Move the bullet."""
        self.position += self.velocity  # Update the position vector.
        self.rect.center = self.position  # And the rect.

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


def main():
    pygame.init()
    pygame.key.set_repeat(500,30)

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen_rect = screen.get_rect()

    all_sprites_list = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()  # "group" not "list".

    player = Player()
    all_sprites_list.add(player)

    MAXSPEED = 15
    MINSPEED = -5

    clock = pygame.time.Clock()

    done = False
    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.speed > MINSPEED:
                    player.speed += 3
                if event.key == pygame.K_DOWN and player.speed < MAXSPEED:
                    player.speed -= 3
                if event.key == pygame.K_LEFT:
                    player.angle_speed = -3
                if event.key == pygame.K_RIGHT:
                    player.angle_speed = 3
                if event.key == pygame.K_SPACE:
                    # Just pass the rect.center, direction vector and angle.
                    bullet = Bullet(
                        player.rect.center, player.direction, player.angle)
                    all_sprites_list.add(bullet)
                    bullet_group.add(bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.angle_speed = 0
                elif event.key == pygame.K_RIGHT:
                    player.angle_speed = 0

        all_sprites_list.update()
        player.rect.clamp_ip(screen_rect)

        screen.fill(WHITE)
        all_sprites_list.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.quit()