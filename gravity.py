import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((700, 700))

white   = (255, 255, 255)
black   = (000, 000, 000)
red     = (255, 000, 000)

clock = pygame.time.Clock()

#circle = pygame.Surface((30, 30,))

running = True
ship_img = pygame.image.load('playerShip1_red.png')


def addVectors(angle1_length1, angle2_length2):
    angle1, length1 = angle1_length1
    angle2, length2 = angle2_length2
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)


def draw_spaceship(x, y, angle):
    magnitude = 30
    p1_angle = angle
    p2_angle = angle + math.radians(145)
    p3_angle = angle - math.radians(145)
    p1 = (math.cos(p1_angle) * magnitude + x, -math.sin(p1_angle) * magnitude + y)
    p2 = (math.cos(p2_angle) * magnitude + x, -math.sin(p2_angle) * magnitude + y)
    p3 = (math.cos(p3_angle) * magnitude + x, -math.sin(p3_angle) * magnitude + y)

    pygame.draw.line(screen, white, (p1[0], p1[1]), (p2[0], p2[1]))
    pygame.draw.line(screen, white, (p1[0], p1[1]), (p3[0], p3[1]))
    pygame.draw.line(screen, white, (p2[0], p2[1]), (p3[0], p3[1]))
    pygame.draw.circle(screen, red, (int(x), int(y)), 1)

    screen.blit(ship_img, (x, y))

angle = math.pi / 2
angle_change = 0
trajectory_angle = angle

x, y = 350, 350

speed = 0
thrust = 0
max_speed = 12

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_change = .03
            elif event.key == pygame.K_RIGHT:
                angle_change = -.03
            elif event.key == pygame.K_UP:
                thrust = .04

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                angle_change = 0
            elif event.key == pygame.K_RIGHT:
                angle_change = 0
            elif event.key == pygame.K_UP:
                thrust = 0

    screen.fill(black)

    # this is the direction the spaceship is pointing
    angle += angle_change

    # the trajectory angle is the angle that the spaceship is moving, not the
    # angle it is pointing. if the player is pressing the up key, a vector
    # will be added to change the direciton and speed
    trajectory_angle, speed = addVectors((trajectory_angle, speed),
                                            (angle, thrust))

    # this just limits the speed of the spaceship
    if speed > max_speed:
        speed = max_speed

    # update the position of the spaceship
    x += math.cos(trajectory_angle) * speed
    y -= math.sin(trajectory_angle) * speed

    # make the spaceship appear on the other side of the it goes beyond the
    # screen

    # make the spaceship appear on the other side if it goes beyond the screen
    x %= 760
    y %= 760

    draw_spaceship(x, y, angle)
    print('trajectory_angle:', trajectory_angle, 'speed:', speed,
          'angle:', angle, 'thrust:', thrust, 'angle_chane:', angle_change,
          'function return:', addVectors((trajectory_angle, speed), (angle, thrust)))
    pygame.display.flip()

    clock.tick(90)

pygame.quit()