import sys
import pygame


class Star(pygame.sprite.Sprite):
    """A class to represent a single star in the sky."""

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # Load the star image and set its rect.
        self.image = pygame.image.load("images/star.bmp")
        self.rect = self.image.get_rect()

        # Start each new star near the top-left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stars")

    # Make a group to store all the stars.
    stars = pygame.sprite.Group()

    # Create the grid of stars.
    _create_star_grid(screen, stars)

    # Main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Redraw the screen.
        screen.fill((0, 0, 0))  # Black background
        stars.draw(screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


def _create_star_grid(screen, stars):
    """Create a full grid of stars that fits on the screen."""
    # Make a star just to get its size.
    star = Star(screen)
    star_width, star_height = star.rect.size

    screen_rect = screen.get_rect()

    # Compute how many stars fit in a row.
    available_space_x = screen_rect.width - 2 * star_width
    number_stars_x = available_space_x // (2 * star_width)

    # Compute how many rows of stars fit on the screen.
    available_space_y = screen_rect.height - 2 * star_height
    number_rows = available_space_y // (2 * star_height)

    # Create the full grid.
    for row_number in range(number_rows):
        for star_number in range(number_stars_x):
            _create_star(screen, stars, star_number, row_number, star_width, star_height)


def _create_star(screen, stars, star_number, row_number, star_width, star_height):
    """Create a star and place it in the grid."""
    star = Star(screen)
    star.x = star_width + 2 * star_width * star_number
    star.rect.x = star.x

    star.y = star_height + 2 * star_height * row_number
    star.rect.y = star.y

    stars.add(star)


if __name__ == "__main__":
    run_game()
