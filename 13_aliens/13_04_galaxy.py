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

        # Default starting position (will be reset when placed in grid).
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store decimal position for smooth movement.
        self.y = float(self.rect.y)

        # Falling speed in pixels per frame.
        self.speed_factor = 1.0

    def update(self):
        """Move the raindrop downward."""
        self.y += self.speed_factor
        self.rect.y = self.y


# Globals to keep track of grid layout
NUMBER_DROPS_X = 0
NUMBER_ROWS = 0
DROP_WIDTH = 0
DROP_HEIGHT = 0


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Steady Rain")

    raindrops = pygame.sprite.Group()

    # Create initial grid and set up global layout variables.
    _create_raindrop_grid(screen, raindrops)

    while True:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update raindrops.
        raindrops.update()

        # Remove drops that have moved off bottom of the screen.
        screen_rect = screen.get_rect()
        for raindrop in raindrops.copy():
            if raindrop.rect.top >= screen_rect.bottom:
                raindrops.remove(raindrop)

        # Keep the rain steady: when a full row disappears,
        # spawn a new row at the top.
        expected_total = NUMBER_DROPS_X * NUMBER_ROWS
        missing_drops = expected_total - len(raindrops)

        # Each row = NUMBER_DROPS_X drops
        if NUMBER_DROPS_X > 0 and missing_drops >= NUMBER_DROPS_X:
            missing_rows = missing_drops // NUMBER_DROPS_X
            for _ in range(missing_rows):
                _create_top_row(screen, raindrops)

        # Draw everything.
        screen.fill((0, 0, 0))  # dark background
        raindrops.draw(screen)
        pygame.display.flip()


def _create_raindrop_grid(screen, raindrops):
    """Create a grid of raindrops across the screen and
    set global layout values."""
    global NUMBER_DROPS_X, NUMBER_ROWS, DROP_WIDTH, DROP_HEIGHT

    sample_raindrop = Raindrop(screen)
    DROP_WIDTH, DROP_HEIGHT = sample_raindrop.rect.size
    screen_rect = screen.get_rect()

    # How many raindrops fit in a row?
    available_space_x = screen_rect.width - 2 * DROP_WIDTH
    NUMBER_DROPS_X = available_space_x // (2 * DROP_WIDTH)

    # How many rows fit on the screen?
    available_space_y = screen_rect.height - 2 * DROP_HEIGHT
    NUMBER_ROWS = available_space_y // (2 * DROP_HEIGHT)

    for row in range(NUMBER_ROWS):
        for drop_number in range(NUMBER_DROPS_X):
            _create_raindrop(
                screen, raindrops, drop_number, row, DROP_WIDTH, DROP_HEIGHT
            )


def _create_raindrop(screen, raindrops, drop_number, row_number, drop_width, drop_height):
    """Create a raindrop and place it in the initial grid."""
    raindrop = Raindrop(screen)

    raindrop.rect.x = drop_width + 2 * drop_width * drop_number
    raindrop.y = drop_height + 2 * drop_height * row_number
    raindrop.rect.y = raindrop.y

    raindrops.add(raindrop)


def _create_top_row(screen, raindrops):
    """Create a new row of raindrops just above the top of the screen."""
    for drop_number in range(NUMBER_DROPS_X):
        raindrop = Raindrop(screen)

        # Same x spacing as grid:
        raindrop.rect.x = DROP_WIDTH + 2 * DROP_WIDTH * drop_number

        # Start just above the visible area so they "fall into" the screen.
        raindrop.y = -DROP_HEIGHT
        raindrop.rect.y = raindrop.y

        raindrops.add(raindrop)


if __name__ == "__main__":
    run_game()
