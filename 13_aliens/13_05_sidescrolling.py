import sys
import pygame


class Settings:
    """Store settings for Sideways Shooter."""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed = 1.0


class Ship:
    """Ship that moves up and down on the left side of the screen."""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position."""
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at left center.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update ship's position based on movement flags."""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def blitme(self):
        """Draw ship at its current location."""
        self.screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """Bullet fired from the ship toward the right."""

    def __init__(self, ss_game):
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midleft = ss_game.ship.rect.midright

        # Store bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move bullet to the right."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw bullet on screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(pygame.sprite.Sprite):
    """Alien that starts on the right and moves left toward the ship."""

    def __init__(self, ss_game):
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        # Load alien image and set its rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each alien somewhere on the right; exact position set later.
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's horizontal position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move alien left."""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)


class SidewaysShooter:
    """Overall class to manage game behavior and assets."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Sideways Shooter")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    # --- Event handling ---

    def _check_events(self):
        """Respond to keypresses and other events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Handle keydown events."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        """Handle keyup events."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # --- Bullets ---

    def _fire_bullet(self):
        """Create a new bullet and add to bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullet positions and remove old bullets."""
        self.bullets.update()

        # Remove bullets that have gone off right edge.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        # Check for collisions between bullets and aliens.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        # If fleet is destroyed, create a new fleet.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    # --- Aliens ---

    def _create_fleet(self):
        """Create a fleet of aliens on the right side of the screen."""
        # Create an alien and find number of aliens in a column and rows.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Space for fleet on the right side, leaving room for the ship on the left.
        available_space_x = (
            self.settings.screen_width
            - (3 * alien_width)
            - self.ship.rect.width
        )
        number_columns = available_space_x // (2 * alien_width)

        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for column_number in range(number_columns):
                self._create_alien(
                    column_number, row_number, alien_width, alien_height
                )

    def _create_alien(
        self, column_number, row_number, alien_width, alien_height
    ):
        """Create an alien and place it in the fleet."""
        alien = Alien(self)

        # Start from the right and move leftward for each column.
        x = (
            self.settings.screen_width
            - alien_width
            - 2 * alien_width * column_number
        )
        y = alien_height + 2 * alien_height * row_number

        alien.x = float(x)
        alien.rect.x = x
        alien.rect.y = y

        self.aliens.add(alien)

    def _update_aliens(self):
        """Update positions of all aliens in the fleet."""
        self.aliens.update()

        # If any alien reaches the left edge, reset fleet.
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Here you could also end game; for now just reset.
                self.aliens.empty()
                self.bullets.empty()
                self._create_fleet()
                break

    # --- Drawing ---

    def _update_screen(self):
        """Redraw all elements on the screen."""
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    ss = SidewaysShooter()
    ss.run_game()
