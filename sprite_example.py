# Pygame template - skeleton for a new pygame project
import pygame
import random
import os


WIDTH = 800
HIEGHT = 600
FPS = 30

# define colors RGB
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255,0)
BLUE = (0,0,255)


# set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")



# initalize pygame and create window
pygame.init()
pygame.mixer.init() # initilized mixer to handle any sound in games
screen = pygame.display.set_mode((WIDTH, HIEGHT))
pygame.display.set_caption("My GAME")
clock = pygame.time.Clock()


# our sprite
class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # paranet init need for sprit to fucntion porperly
        # must have image, and rect
        self.image = pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert() #.convert() converst to format pygame can use, will run without .convert() but game will be much slower
        self.image.set_colorkey(BLACK) # sets black around img to be transparent, ie so the image doesn't have a background
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HIEGHT/2) # put the center of the rectangel in the midle of the screen
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HIEGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # after drawing everying, flip the display
    pygame.display.flip() # for double buffering



pygame.quit()