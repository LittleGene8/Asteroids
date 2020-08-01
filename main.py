import pygame
from pathlib import Path

pygame.init()

# Create a window

window = pygame.display.set_mode((800, 600))

# Player

player_img = pygame.image.load('Assets/player.png')
playerX = 380
playerY = 280

# Colors

black = (0,0,0)

# Game Variables
run = True

# Draw Function

def draw():

  window.blit(player_img, (playerX, playerY))

# Game Loop

while run:

  window.fill(black)

  draw()

  pygame.display.update()

  for event in pygame.event.get():
    if event == pygame.QUIT:
      run = False