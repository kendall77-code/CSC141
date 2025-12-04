import sys
import pygame


class Raindrop(pygame.sprite.Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # Load the raindrop image and set its rect.
        self.image = pygame.image.load("images/raindrop.bmp")
        self.rect = self.image.get_rect()

        # Start each new raindrop near the top-left by default.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store decimal positions for fine movement.
        self.y = float(self.rect.y)

        # How fast the raindrops fall (pixels per frame).
        self.speed_factor = 1.0

    def update(self):
        """Move the raindrop downward."""
        self.y += self.speed_factor
        self.rect.y = self.y


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Raindrops")

    # Group for all raindrops.
    raindrops = pygame.sprite.Group()

    # Create the initial grid of raindrops.
    _create_raindrop_grid(screen, raindrops)

    # Main loop.
    while True:
        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update raindrops.
        raindrops.update()

        # Remove any raindrops that have moved off the bottom of the screen.
        screen_rect = screen.get_rect()
        for raindrop in raindrops.copy():
            if raindrop.rect.top >= screen_rect.bottom:
                raindrops.remove(raindrop)

        # Draw everything.
        screen.fill((0, 0, 0))  # optional: dark background
        raindrops.draw(screen)

        pygame.display.flip()


def _create_raindrop_grid(screen, raindrops):
    """Create a grid of raindrops across the screen."""
    sample_raindrop = Raindrop(screen)
    drop_width, drop_height = sample_raindrop.rect.size
    screen_rect = screen.get_rect()

    # How many raindrops fit in a row?
    available_space_x = screen_rect.width - 2 * drop_width
    number_drops_x = available_space_x // (2 * drop_width)

    # How many rows of raindrops fit on the screen?
    available_space_y = screen_rect.height - 2 * drop_height
    number_rows = available_space_y // (2 * drop_height)

    for row in range(number_rows):
        for drop_number in range(number_drops_x):
            _create_raindrop(
                screen, raindrops, drop_number, row, drop_width, drop_height
            )


def _create_raindrop(screen, raindrops, drop_number, row_number, drop_width, drop_height):
    """Create a raindrop and place it in the grid."""
    raindrop = Raindrop(screen)

    raindrop.rect.x = drop_width + 2 * drop_width * drop_number
    raindrop.y = drop_height + 2 * drop_height * row_number
    raindrop.rect.y = raindrop.y

    raindrops.add(raindrop)


if __name__ == "__main__":
    run_game()
