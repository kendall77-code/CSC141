# Updated from Irv Kalb Chapter 5 example
# This program is a game where you click the ball 5 times

import pygame
import random
import sys

pygame.init()

# window stuff
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Ball Click Game")

clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# fonts
font = pygame.font.SysFont(None, 30)
bigFont = pygame.font.SysFont(None, 45)

# ball variables
ballSize = 25
ballX = random.randint(ballSize, screenWidth - ballSize)
ballY = random.randint(ballSize, screenHeight - ballSize)

xSpeed = 3
ySpeed = -3

ballRect = pygame.Rect(ballX, ballY, ballSize * 2, ballSize * 2)

# game variables
score = 0
startTime = pygame.time.get_ticks()
finishTime = 0
done = False

running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if done == False:
                mouseX, mouseY = pygame.mouse.get_pos()

                if ballRect.collidepoint(mouseX, mouseY):
                    score = score + 1

                    # move ball to random spot
                    ballX = random.randint(ballSize, screenWidth - ballSize)
                    ballY = random.randint(ballSize, screenHeight - ballSize)

                    # make ball faster
                    xAdd = random.randint(1, 5)
                    yAdd = random.randint(1, 5)

                    if xSpeed < 0:
                        xSpeed = -abs(xSpeed + xAdd)
                    else:
                        xSpeed = abs(xSpeed + xAdd)

                    if ySpeed < 0:
                        ySpeed = -abs(ySpeed + yAdd)
                    else:
                        ySpeed = abs(ySpeed + yAdd)

                    if score >= 5:
                        done = True
                        finishTime = pygame.time.get_ticks()

    if done == False:
        # move ball
        ballX = ballX + xSpeed
        ballY = ballY + ySpeed

        if ballX <= 0 or ballX + ballSize * 2 >= screenWidth:
            xSpeed = -xSpeed

        if ballY <= 0 or ballY + ballSize * 2 >= screenHeight:
            ySpeed = -ySpeed

        ballRect.x = ballX
        ballRect.y = ballY

        pygame.draw.circle(
            screen,
            RED,
            (ballX + ballSize, ballY + ballSize),
            ballSize
        )

        scoreText = font.render("Score: " + str(score), True, BLACK)
        screen.blit(scoreText, (10, 10))

    else:
        totalTime = (finishTime - startTime) / 1000
        endText = bigFont.render("Game Over", True, BLACK)
        timeText = font.render(
            "It took " + str(totalTime) + " seconds", True, BLACK)

        screen.blit(
            endText,
            (screenWidth // 2 - 100, screenHeight // 2 - 40)
        )
        screen.blit(
            timeText,
            (screenWidth // 2 - 150, screenHeight // 2 + 10)
        )

    pygame.display.update()

pygame.quit()
sys.exit()
