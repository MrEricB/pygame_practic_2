# Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 360
HIEGHT = 480
FPS = 30

# define colors RGB
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255,0)
BLUE = (0,0,255)


# initalize pygame and create window
pygame.init()
pygame.mixer.init() # initilized mixer to handle any sound in games
screen = pygame.display.set_mode((WIDTH, HIEGHT))
pygame.display.set_caption("My GAME")
clock = pygame.time.Clock()



all_sprites = pygame.sprite.Group()

# Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    #### Process input (events)
    for event in pygame.event.get(): # any events since last time we ask for events
        # check for closing widnow
        if event.type == pygame.QUIT:
            running = False

    #### update
    all_sprites.update()

    #### draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing everying, flip the display
    pygame.display.flip() # for double buffering



pygame.quit()