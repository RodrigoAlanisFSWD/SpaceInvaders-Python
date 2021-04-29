import pygame
from pygame.constants import K_RIGHT
import random
import math
from pygame import mixer

# Initialize the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon 
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("./player.png")
playerX = 360
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.35)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Enemy
laserImg = pygame.image.load("./laser.png")
laserX = 0
laserY = 480
laserY_change = 1
laserX_change = 0
bullet_state = "ready"

def laser(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY , 2)))
    if distance < 27:
        return True
    else:
        return False

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    go_font = pygame.font.Font("freesansbold.ttf", 64)
    text = go_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))
# Game Loop
running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard Input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    laser_sound = mixer.Sound('./laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    laser(laserX, laserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collison = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collison:
            col_sound = mixer.Sound('./explosion.wav')
            col_sound.play()
            laserY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i], enemyY[i], i)
        
    
    if laserY <= 0:
        laserY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        laser(laserX, laserY)
        laserY -= laserY_change

    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    pass