import pygame
import random
import sys
import math

pygame.init()

# window stuff
screenWidth = 640
screenHeight = 480
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Too Many Balls")
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)


def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


# ball settings
ballList = []
minRadius = 12
maxRadius = 24

# game variables
score = 0
lastSeconds = 0
startTicks = pygame.time.get_ticks()
lastTicks = startTicks

gameOver = False

# add a starting ball so it's not empty
ballList.append((random.randint(30, screenWidth - 30),
                 random.randint(30, screenHeight - 30),
                 random.randint(minRadius, maxRadius)))

running = True
while running:
    clock.tick(60)
    window.fill(WHITE)

    currentTicks = pygame.time.get_ticks()
    secondsElapsed = (currentTicks - startTicks) // 1000
    tickDiff = (currentTicks - lastTicks) // 1000  # a little redundant but ok
    lastTicks = currentTicks

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mouseX, mouseY = pygame.mouse.get_pos()
            hitIndex = -1
            for i, ball in enumerate(ballList):
                bx, by, br = ball
                dist = math.hypot(mouseX - bx, mouseY - by)
                if dist <= br:
                    hitIndex = i
                    break

            if hitIndex >= 0:
                score = score + 1
                ballList.pop(hitIndex)

    if not gameOver:
        # add new balls each second that passes
        if secondsElapsed > lastSeconds:
            for _ in range(secondsElapsed - lastSeconds):
                ballList.append((
                    random.randint(30, screenWidth - 30),
                    random.randint(30, screenHeight - 30),
                    random.randint(minRadius, maxRadius)
                ))
            lastSeconds = secondsElapsed

        # draw balls
        for ball in ballList:
            bx, by, br = ball
            pygame.draw.circle(window, BLUE, (bx, by), br)

        draw_text(window, "Score: " + str(score), 10, 10, BLACK, 24)
        draw_text(window, "Seconds: " + str(secondsElapsed), 10, 38, BLACK, 22)

        if secondsElapsed >= 15:
            gameOver = True
            ballList.clear()
    else:
        # final screen
        draw_text(window, "Game Over", screenWidth // 2 - 60, screenHeight // 2 - 20, BLACK, 36)
        draw_text(window, "Final score: " + str(score), screenWidth // 2 - 80, screenHeight // 2 + 20, BLACK, 24)

    pygame.display.update()

pygame.quit()
sys.exit()
