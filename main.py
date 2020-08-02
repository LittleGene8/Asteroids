#Asteroids Game

import pygame
import math

pygame.init()

# Create a window

window = pygame.display.set_mode((800, 600))

# Player

player_img = pygame.image.load('Assets/player.png')
playerX = 400
playerY = 280
playerX_change = 0
playerY_change = 0
player_angle = 90
play_ang_change = 0

# Colors

black = (0, 0, 0)

# Game Variables
run = True


# Game Functions


def get_speeds(ang, vel):
    ang_rad = math.radians(ang)
    vel_x = math.cos(ang_rad) * vel
    vel_y = math.sin(ang_rad) * vel
    return (vel_x, vel_y)


def draw():
    global player_angle
    global playerX
    global playerY

    # Player

    player_img_copy = pygame.transform.rotozoom(player_img, player_angle, 1)  # rotates player

    # Determines amount to subtract by to center
    center_x = player_img_copy.get_width() / 2
    center_y = player_img_copy.get_height() / 2

    window.blit(player_img_copy, (playerX - center_x, playerY - center_y))  # centers and draws image

    player_angle += play_ang_change  # Adds onto angle based on controls
    playerX += playerX_change
    playerY -= playerY_change


# Game Loop

while run:

    window.fill(black)

    draw()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                play_ang_change = 7.5
            if event.key == pygame.K_RIGHT:
                play_ang_change = -7.5
            if event.key == pygame.K_UP:
                playerX_change, playerY_change = get_speeds(player_angle, 3)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                play_ang_change = 0
            if event.key == pygame.K_UP:
                playerX_change, playerY_change = 0, 0
