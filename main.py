import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# Create the Screen Size 1366 x 788
screen = pygame.display.set_mode((1366, 788))

# Init Background
background = pygame.image.load('Assets/img/bg_main.jpg')
background = pygame.transform.scale(background, (1366, 788))

# Init Background Sound
mixer.music.load('Assets/sound/bgm.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Assets/img/spaceship.png')
pygame.display.set_icon(icon)

# Player 
playerImg = pygame.image.load('Assets/img/player.png')
playerX = 645
playerY = 550
speedX = 1.5
speedY = 1

# New width and height for player will be (60, 60)
player_resize = pygame.transform.scale(playerImg, (60, 60))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_resize = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Assets/img/enemy.png'))
    enemyX.append(random.randint(0, 1323))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(30)
    enemy_resize.append(pygame.transform.scale(enemyImg[i], (80, 80)))

# Bullet
bulletImg = pygame.image.load('Assets/img/bullet.png')
bulletX = 0
bulletY = playerY - 10
bulletX_change = 0
bulletY_change = 3
bullet_resize = pygame.transform.scale(bulletImg, (32, 32))

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# Init Score
score_value = 0
font = pygame.font.Font('Assets/font/evil_empire.otf', 64)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('Assets/font/evil_empire.otf', 1024)


# Function Player
def player(x, y):
    screen.blit(player_resize, (x, y))  # Drop player to screenGame

# Function Enemy
def enemy(x, y, i):
    screen.blit(enemy_resize[i], (x, y))  # Drop enemy to screenGame

# Function Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_resize, (x + 16, y + 16))  # Drop bullet to screenGame

# Function Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 28:
        return True
    else:
        return False

# Show Score Game
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

# Show Game Over
def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (550,350))

# Draw Dashed Line
def draw_dashed_line(y, color, dash_length=10):
    x_start = 0
    while x_start < 1366:
        pygame.draw.line(screen, color, (x_start, y), (x_start + dash_length, y))
        x_start += 2 * dash_length

# Game Loop
running = True
while running:
    # Add blackBG
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Draw Dashed Line
    draw_dashed_line(350, (255, 255, 255))

    # Player Movement
    keys = pygame.key.get_pressed()
    playerX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speedX
    playerY += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speedY

    # Boundaries player inside screen and above Y = 350
    playerX = max(0, min(playerX, 1323))
    playerY = max(350, min(playerY, 750))

    # Bullet Trigger
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_Sound = mixer.Sound('Assets/sound/shoot.wav')
            bullet_Sound.play()
            # Get the current x coordinate of the spaceship
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    # Bullet Movement
    if bulletY < -20:
        bulletY = playerY - 10
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Boundaries player inside screen
    playerX = max(0, min(playerX, 1323))
    playerY = max(0, min(playerY, 750))

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 3000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Check boundaries and update direction and position
        if enemyX[i] <= 0 or enemyX[i] >= 1323:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('Assets/sound/explosion.wav')
            explosion_Sound.play()
            bulletY = playerY - 10
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1323)
            enemyY[i] = random.randint(50, 70)
            enemyX_change[i] *= 1.5
            # print(enemyX_change)

        # Reset enemy speed if it exceeds 3.5 or is less than -3.5
        if enemyX_change[i] >= 4 or enemyX_change[i] <= -4:
            enemyX_change[i] = 0.7 if enemyX_change[i] > 0 else -0.7

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX,textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
