# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

# Art from Kenny.nl
import pygame
import random
from os import path


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors RGB
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)


# initalize pygame and create window
pygame.init()
pygame.mixer.init() # initilized mixer to handle any sound in games
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!!!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial') #pygame will find the closest match on a given computer
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20 # radius variable is need (name specific) for pygmae to do circle collision detections
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed() # gives back list of every key that is down this instence
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        # copy used for rotation
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # location and speed where the enemy/Mob spawns
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0 # how fare in degrees the sprit should be rotated
        self.rot_speed = random.randrange(-8,8)
        self.last_updated = pygame.time.get_ticks() # how long since last rotated image

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 50: # in milliseconds
            self.last_updated = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: # wrap back around the screen ie back to top
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #spawn infron of player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if moves off top of screen
        if self.rect.bottom < 0:
            self.kill() # kill is command that removes and deltes sprite and deltes from any goups it is in


# load game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_med1.png','meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_small2.png','meteorBrown_tiny1.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# load game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
exlp_sounds = []
for snd in ['expl4.wav', 'expl5.wav']:
    exlp_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# background music
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #### update ####
    all_sprites.update()
        # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # takes two groups
        #check to see if mob hit the player
    for hit in hits:
        score += 50 -hit.radius #this way smaller ones are worth more points
        random.choice(exlp_sounds).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) # takes sprite and a group who to check, who to check against, bool what hit should be deleted or not; gives back list
    if hits:
        running = False
    #### draw / render ####
    screen.fill(BLACK)
    screen.blit(background, background_rect) # need to manually blit unlike below in all_sprites
    all_sprites.draw(screen) # all_sprits.draw automaticly blits for you
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    # after drawing everying, flip the display
    pygame.display.flip() # for double buffering

pygame.quit()


