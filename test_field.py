import math
import pygame


pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

BULLET_IMAGE = pygame.Surface((20, 11), pygame.SRCALPHA)
pygame.draw.polygon(BULLET_IMAGE, pygame.Color('aquamarine1'),
                [(0, 0), (20, 5), (0, 11)])


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, angle, speed):
        pygame.sprite.Sprite.__init__(self)
        # Rotate the bullet image (negative angle because y-axis is flipped).
        self.image = pygame.transform.rotate(BULLET_IMAGE, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.radians(angle)
        self.speed_x = speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

spr = pygame.sprite.Group()
bullet = Bullet(10, 10, 60, 3)
bullet2 = Bullet(10, 10, 30, 3)
spr.add(bullet, bullet2)

play = True
while play:
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            play = False
    screen.fill((30,30,40))
    spr.update()
    spr.draw(screen)
    pygame.display.flip()

pygame.quit()