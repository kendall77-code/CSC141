import sys
import pygame


class GameCharacter:
    """A simple game character that appears at the center of the screen."""

    def __init__(self, screen):
        """Load the character image and set its starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Load the character image.
        self.image = pygame.image.load("images/character.bmp")
        self.rect = self.image.get_rect()

        # Start the character at the center of the screen.
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.rect)


def run_game():
    # Initialize pygame
    pygame.init()

    # Screen settings
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Character")

    # Match this background color with the background color of character.bmp
    bg_color = (135, 206, 235)  # light sky blue, for example

    # Make a character instance.
    character = GameCharacter(screen)

    # Main loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen and draw character
        screen.fill(bg_color)
        character.blitme()

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    run_game()
