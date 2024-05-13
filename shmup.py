# Shmup game
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 480
HEIGHT = 600
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, width=1)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx -= 8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.radius = self.rect.width * 0,85 / 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, width=1)
        self.rect.x = random.randrange(WIDTH - self.rect.width) # 480 - 30 = 450 --> 0 ~ 449
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 4)
        self.sppedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.sppedy
        if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width) # 480 - 30 = 450 --> 0 ~ 449
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 4)
            self.sppedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()        
        self.image = bullet_img
        self.image.set_colorkey (BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    # Keep loop runnging at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False) # pygame.sprite.collide_circle
    if hits:
        running = False 

    # Draw / render
    screen.blit(background, background_rect)
    
    # Draw everything
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
