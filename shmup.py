# Shmup game
import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
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


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
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


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

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

    # Update
    all_sprites.update()

    hits= pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False 

    # Draw / render
    screen.fill(BLACK)
    # Draw everything
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
