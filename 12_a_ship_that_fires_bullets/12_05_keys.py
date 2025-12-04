import sys
import pygame


def run_game():
    pygame.init()

    # Create a simple empty screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Key Tester")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detect key press events
            if event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")

        # Fill screen with black
        screen.fill((0, 0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
