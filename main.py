import pygame

pygame.init()

# Create a window

window = pygame.display.set_mode((800, 600))

# Colors

black = (0,0,0)

# Game Variables
run = True

# Game Loop

while run:

  window.fill(black)

  for event in pygame.event.get():
    if event == pygame.QUIT:
      run = False

  pygame.display.update()
