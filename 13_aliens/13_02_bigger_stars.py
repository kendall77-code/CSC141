import sys
import pygame
from random import randint


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
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Better Stars")

    stars = pygame.sprite.Group()
    _create_star_grid(screen, stars)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        stars.draw(screen)
        pygame.display.flip()


def _create_star_grid(screen, stars):
    """Create a grid of stars with random position offsets."""
    sample_star = Star(screen)
    star_width, star_height = sample_star.rect.size
    screen_rect = screen.get_rect()

    available_space_x = screen_rect.width - 2 * star_width
    number_stars_x = available_space_x // (2 * star_width)

    available_space_y = screen_rect.height - 2 * star_height
    number_rows = available_space_y // (2 * star_height)

    for row in range(number_rows):
        for col in range(number_stars_x):
            _create_random_star(
                screen, stars, col, row, star_width, star_height
            )


def _create_random_star(screen, stars, col, row, star_width, star_height):
    """Create a star and place it with slight randomness."""
    star = Star(screen)

    # Base grid position
    base_x = star_width + 2 * star_width * col
    base_y = star_height + 2 * star_height * row

    # Add random offsets
    offset_x = randint(-20, 20)
    offset_y = randint(-20, 20)

    star.x = base_x + offset_x
    star.rect.x = star.x
    star.y = base_y + offset_y
    star.rect.y = star.y

    stars.add(star)


if __name__ == "__main__":
    run_game()
