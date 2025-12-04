import sys
import pygame

def run_game():
    # Initialize pygame
    pygame.init()

    # Create the screen (width, height)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Blue Sky")

    # Define a blue color (R, G, B)
    blue = (135, 206, 235)   # Sky blue

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with blue
        screen.fill(blue)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    run_game()
