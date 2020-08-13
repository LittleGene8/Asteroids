# Asteroids Game

import pygame
import math
import os.path
from random import *

pygame.init()

# Create a window

window = pygame.display.set_mode((800, 600))

# Player

player_img = pygame.image.load(os.path.join('Assets', 'player.png'))
playerX = 400
playerY = 280
playerX_change = 0
playerY_change = 0
player_angle = 90
play_ang_change = 0
speed = 3

# Colors

black = (0, 0, 0)

# Game Variables
run = True
drag = False
clock = pygame.time.Clock()
score = 0

# Score
pygame.font.init()

score_font = pygame.font.SysFont('Comic Sans MS', 30)


# Game Functions


def get_speeds(ang, vel):
    ang_rad = math.radians(ang)
    vel_x = math.cos(ang_rad) * vel
    vel_y = math.sin(ang_rad) * vel
    return [vel_x, vel_y]


# Bullet

bullets = []


class Bullet:

    def __init__(self, ang, x, y):
        bullets.append(self)
        self.img = pygame.image.load(os.path.join('Assets', 'missile.png'))
        self.angle = ang
        self.pos_x = x
        self.pos_y = y
        self.x_change = 0
        self.y_change = 0
        self.state = 'ready'
        self.speed = 4.5

    def fire_bullet(self):
        self.state = 'fire'
        self.x_change, self.y_change = get_speeds(self.angle, self.speed)


# Asteroid

asteroids = []


class Asteroid:

    def __init__(self, size):
        asteroids.append(self)
        self.img = pygame.image.load(os.path.join('Assets', 'asteroid_' + str(size) + '.png'))
        self.angle = Random.randint(Random(), 0, 360)
        self.pos_x = Random.randint(Random(), 0, 800)
        self.pos_y = Random.randint(Random(), 0, 600)
        self.x_change = 0
        self.y_change = 0
        self.size = size
        # ready --> not on screen, intact --> on screen hasn't been hit, destroyed
        self.state = 'ready'
        self.speed = 1.5

    def create_asteroid(self):
        self.state = 'intact'
        self.x_change, self.y_change = get_speeds(self.angle, self.speed)


def baby_asteroids(instance):
    global asteroids

    if instance.state == 'destroyed':
        if instance.size == 'large':
            for i in range(2):
                Asteroid('medium')
                asteroids[-1].create_asteroid()
        elif instance.size == 'medium':
            for i in range(3):
                Asteroid('small')
                asteroids[-1].create_asteroid()

        asteroids.remove(instance)

            # Player Collision function


def is_collision(x1, y1, x2, y2, gap):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance <= gap:
        return True
    return False


def draw():
    global player_angle
    global playerX
    global playerY
    global speed
    global playerX_change
    global playerY_change
    global score

    # Draw Score

    text = score_font.render('Score: ' + str(score), True, (255, 255, 255))
    window.blit(text, (0, 0))

    # Asteroids

    for asteroid in asteroids:

        for bullet in bullets:
            if is_collision(bullet.pos_x, bullet.pos_y, asteroid.pos_x, asteroid.pos_y, 70):
                score += 1
                bullet.state = 'ready'
                bullets.remove(bullet)
                asteroid.state = 'destroyed'
                baby_asteroids(asteroid)

        asteroid.angle += 1

        if asteroid.state == 'intact':
            # Allows asteroid to move through the screen
            asteroid.pos_x += asteroid.x_change
            asteroid.pos_y -= asteroid.y_change

            # Centers the asteroid image
            asteroid.img_copy = pygame.transform.rotozoom(asteroid.img, asteroid.angle, 1)

            # Draws bullet img
            window.blit(asteroid.img_copy, (
                asteroid.pos_x - asteroid.img_copy.get_width() / 2, asteroid.pos_y - asteroid.img_copy.get_height() / 2)
                        )

            # Boundaries
            if asteroid.pos_x <= -150 or asteroid.pos_x >= 1000:
                asteroid.state = 'ready'
                asteroids.remove(asteroid)
            if asteroid.pos_y <= -150 or asteroid.pos_y >= 700:
                asteroid.state = 'ready'
                asteroids.remove(asteroid)

    # Player

    player_img_copy = pygame.transform.rotozoom(player_img, player_angle, 1)  # rotates player

    # Determines amount to subtract by to center
    center_x = player_img_copy.get_width() / 2
    center_y = player_img_copy.get_height() / 2

    # centers and draws image
    window.blit(player_img_copy, (playerX - center_x, playerY - center_y))

    # Bullet

    for bullet in bullets:

        if bullet.state == 'fire':
            # Allows bullet to "move" through the screen
            bullet.pos_x += bullet.x_change
            bullet.pos_y -= bullet.y_change

            # Centers the bullet image
            bullet.img_copy = pygame.transform.rotozoom(bullet.img, bullet.angle, 1)

            # Draws bullet img
            window.blit(bullet.img_copy, (
                bullet.pos_x - bullet.img_copy.get_width() / 2, bullet.pos_y - bullet.img_copy.get_height() / 2)
                        )

            if not 0 < bullet.pos_x < 800 or not 0 < bullet.pos_y < 600:
                bullet.state = 'ready'
                bullets.remove(bullet)

    # Drag

    if drag:
        speed *= 0.99
        playerX_change, playerY_change = get_speeds(temp_angle, speed)

    player_angle += play_ang_change  # Adds onto angle based on controls
    playerX += playerX_change
    playerY -= playerY_change

    # Adding Boundaries

    if playerX <= 16:
        playerX = 16
    if playerX >= 780:
        playerX = 780
    if playerY <= 16:
        playerY = 16
    if playerY >= 580:
        playerY = 580


# Game Loop
while run:

    clock.tick(60)

    # Screen background
    window.fill(black)

    draw()

    pygame.display.update()

    # Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                play_ang_change = 6
            if event.key == pygame.K_RIGHT:
                play_ang_change = -6
            if event.key == pygame.K_UP:
                drag = False
                speed = 2.5
                playerX_change, playerY_change = get_speeds(player_angle, speed)
            if event.key == pygame.K_SPACE:
                Bullet(player_angle, playerX, playerY)
                bullets[-1].fire_bullet()
            if event.key == pygame.K_x:
                Asteroid('large')
                asteroids[-1].create_asteroid()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                play_ang_change = 0
            if event.key == pygame.K_UP:
                temp_angle = player_angle
                drag = True
