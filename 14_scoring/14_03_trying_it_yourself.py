import sys
import pygame


class Settings:
    """Store settings for Target Practice game."""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (30, 30, 30)

        # Ship settings
        self.ship_speed = 3.0
        self.ship_width = 20
        self.ship_height = 80
        self.ship_color = (50, 200, 50)

        # Bullet settings
        self.bullet_speed = 6.0
        self.bullet_width = 20
        self.bullet_height = 4
        self.bullet_color = (240, 240, 240)
        self.bullets_allowed = 3

        # Target settings
        self.target_speed_base = 2.0
        self.target_speed = self.target_speed_base
        self.target_speed_growth = 1.08
        self.target_width = 40
        self.target_height = 100
        self.target_color = (200, 60, 60)

        # Game rules
        self.max_misses = 3

    def reset_dynamic_settings(self):
        """Return speeds that scale during play to their defaults."""
        self.target_speed = self.target_speed_base

    def increase_target_speed(self):
        """Speed up the target slightly to keep the challenge rising."""
        self.target_speed *= self.target_speed_growth


class GameStats:
    """Track statistics for Target Practice."""

    def __init__(self, tp_game):
        self.settings = tp_game.settings
        self.reset_stats()
        self.game_active = False  # Start with game inactive

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.misses = 0
        self.hits = 0


class Ship:
    """A simple ship that moves up and down on the left side."""

    def __init__(self, tp_game):
        self.screen = tp_game.screen
        self.settings = tp_game.settings
        self.color = self.settings.ship_color

        self.screen_rect = tp_game.screen.get_rect()

        # Create a rect for the ship.
        self.rect = pygame.Rect(
            0, 0, self.settings.ship_width, self.settings.ship_height
        )
        # Start in the center-left of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for precise position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update ship position based on movement flags."""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def center_ship(self):
        """Center the ship vertically."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def draw_ship(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Bullet(pygame.sprite.Sprite):
    """Bullet fired from the ship toward the right."""

    def __init__(self, tp_game):
        super().__init__()
        self.screen = tp_game.screen
        self.settings = tp_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect.
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        # Start at the middle-right of the ship.
        self.rect.midleft = tp_game.ship.rect.midright

        # Store decimal position
        self.x = float(self.rect.x)

    def update(self):
        """Move bullet to the right."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Target:
    """A rectangular target moving up and down at the right edge."""

    def __init__(self, tp_game):
        self.screen = tp_game.screen
        self.settings = tp_game.settings
        self.color = self.settings.target_color

        self.screen_rect = tp_game.screen.get_rect()

        # Create a rect on the right edge.
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.target_width,
            self.settings.target_height,
        )
        self.rect.midright = self.screen_rect.midright

        # Float for precise vertical position.
        self.y = float(self.rect.y)

        # Movement direction: 1 for down, -1 for up
        self.direction = 1

    def update(self):
        """Move the target up and down, bouncing at edges."""
        self.y += self.settings.target_speed * self.direction
        self.rect.y = self.y

        # Bounce when hitting top/bottom.
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = float(self.rect.y)
            self.direction = 1
        elif self.rect.bottom >= self.screen_rect.bottom:
            self.rect.bottom = self.screen_rect.bottom
            self.y = float(self.rect.y)
            self.direction = -1

    def center_target(self):
        """Reset target to vertical center on right edge."""
        self.rect.midright = self.screen_rect.midright
        self.y = float(self.rect.y)
        self.direction = 1

    def draw_target(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Button:
    """A simple Play button."""

    def __init__(self, tp_game, msg):
        self.screen = tp_game.screen
        self.screen_rect = self.screen.get_rect()

        # Button properties
        self.width, self.height = 200, 50
        self.button_color = (0, 200, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        # Build the rect and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Render the message.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center on button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class TargetPractice:
    """Main game class."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Target Practice")

        self.ship = Ship(self)
        self.target = Target(self)
        self.bullets = pygame.sprite.Group()

        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Main loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.target.update()
                self._update_bullets()

            self._update_screen()

    # --- Event Handling ---

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Reset stats and start a new game."""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.settings.reset_dynamic_settings()

        # Clear bullets and reset positions
        self.bullets.empty()
        self.ship.center_ship()
        self.target.center_target()

        pygame.mouse.set_visible(False)

    # --- Bullets and Collisions ---

    def _fire_bullet(self):
        """Create a bullet if limit not reached."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullets and handle collisions & misses."""
        self.bullets.update()

        # Check for collision with target
        for bullet in self.bullets.copy():
            if bullet.rect.colliderect(self.target.rect):
                self.bullets.remove(bullet)
                self.stats.hits += 1
                self.settings.increase_target_speed()
                # Optional: do something on hit, like change target color or reset it
                # Here we'll just continue.

            elif bullet.rect.left >= self.settings.screen_width:
                # Missed the target
                self.bullets.remove(bullet)
                self.stats.misses += 1
                if self.stats.misses >= self.settings.max_misses:
                    self._end_game()

    def _end_game(self):
        """End the game when misses reach max."""
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    # --- Drawing ---

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.ship.draw_ship()
        self.target.draw_target()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw Play button when game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Optionally show misses & hits in title bar
        pygame.display.set_caption(
            f"Target Practice  |  Hits: {self.stats.hits}  Misses: {self.stats.misses}/{self.settings.max_misses}"
        )

        pygame.display.flip()


if __name__ == "__main__":
    game = TargetPractice()
    game.run_game()
