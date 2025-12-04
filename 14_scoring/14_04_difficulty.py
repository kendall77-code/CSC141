import sys
import pygame
from pygame.sprite import Sprite


class Settings:
    """Store all settings for Alien Invasion and its difficulty levels."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 30)

        self.ship_limit = 3
        self.ship_color = (240, 240, 240)

        self.bullet_width = 4
        self.bullet_height = 18
        self.bullet_color = (255, 200, 50)

        self.alien_color = (80, 200, 255)

        self.speedup_scale = 1.1
        self.score_scale = 1.4

        self.difficulty_profiles = {
            "Cadet": {
                "ship_speed": 3.0,
                "bullet_speed": 5.0,
                "alien_speed": 0.6,
                "fleet_drop_speed": 6,
                "bullets_allowed": 6,
                "ship_limit": 4,
                "alien_points": 30,
            },
            "Veteran": {
                "ship_speed": 2.5,
                "bullet_speed": 4.5,
                "alien_speed": 1.0,
                "fleet_drop_speed": 8,
                "bullets_allowed": 4,
                "ship_limit": 3,
                "alien_points": 50,
            },
            "Ace": {
                "ship_speed": 2.0,
                "bullet_speed": 4.0,
                "alien_speed": 1.4,
                "fleet_drop_speed": 10,
                "bullets_allowed": 3,
                "ship_limit": 2,
                "alien_points": 75,
            },
        }
        self.current_difficulty = "Veteran"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Reset dynamic values using the current difficulty profile."""
        profile = self.difficulty_profiles[self.current_difficulty]
        self.ship_speed = profile["ship_speed"]
        self.bullet_speed = profile["bullet_speed"]
        self.alien_speed = profile["alien_speed"]
        self.fleet_drop_speed = profile["fleet_drop_speed"]
        self.bullets_allowed = profile["bullets_allowed"]
        self.ship_limit = profile["ship_limit"]
        self.alien_points = profile["alien_points"]
        self.fleet_direction = 1

    def increase_speed(self):
        """Speed up the game after every fleet is cleared."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, difficulty_name):
        """Apply a difficulty profile and reset dynamic values."""
        if difficulty_name not in self.difficulty_profiles:
            raise ValueError(f"Unknown difficulty: {difficulty_name}")
        self.current_difficulty = difficulty_name
        self.initialize_dynamic_settings()


class GameStats:
    """Track game statistics."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


class Ship:
    """Ship that moves left/right along the bottom."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.width = 60
        self.height = 48
        self.color = self.settings.ship_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Bullet(Sprite):
    """Bullet fired from the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)


class Alien(Sprite):
    """Aliens move in a fleet across the screen."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.width = 50
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.settings.alien_color)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0


class Button:
    """Simple text button used for difficulty selection."""

    def __init__(self, ai_game, msg, center, width=220, height=60, color=(0, 180, 0)):
        self.screen = ai_game.screen
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class AlienInvasion:
    """Main game class with selectable starting difficulties."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion — Difficulty Select")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stats = GameStats(self)

        self.font_small = pygame.font.SysFont(None, 32)
        self.font_large = pygame.font.SysFont(None, 56)

        self.difficulty_buttons = self._build_difficulty_buttons()

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # --- Event handling ---

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
                self._check_difficulty_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_difficulty_buttons(self, mouse_pos):
        if self.stats.game_active:
            return
        for name, button in self.difficulty_buttons.items():
            if button.rect.collidepoint(mouse_pos):
                self._start_game(name)
                break

    def _start_game(self, difficulty_name):
        """Reset game state and apply the chosen difficulty."""
        self.settings.set_difficulty(difficulty_name)
        self.stats.reset_stats()
        self.stats.game_active = True

        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    # --- Bullet handling ---

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in list(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)

        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self._create_fleet()

    # --- Alien handling ---

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = max(1, available_space_y // (2 * alien_height))

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # --- Drawing ---

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.draw()
        self.aliens.draw(self.screen)

        self._draw_hud()

        if not self.stats.game_active:
            self._draw_menu()

        pygame.display.flip()

    def _draw_hud(self):
        caption = (
            f"Alien Invasion — {self.settings.current_difficulty} | "
            f"Score: {self.stats.score}  Level: {self.stats.level}  "
            f"Ships: {self.stats.ships_left}"
        )
        pygame.display.set_caption(caption)

        info = self.font_small.render(
            f"Bullets: {len(self.bullets)}/{self.settings.bullets_allowed}", True, (200, 200, 200)
        )
        self.screen.blit(info, (20, 20))

    def _draw_menu(self):
        title = self.font_large.render("Select Starting Difficulty", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 200))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render(
            "Choose a difficulty to apply balanced settings and jump into battle.",
            True,
            (210, 210, 210),
        )
        subtitle_rect = subtitle.get_rect(center=(self.settings.screen_width // 2, 260))
        self.screen.blit(subtitle, subtitle_rect)

        for button in self.difficulty_buttons.values():
            button.draw_button()

    def _build_difficulty_buttons(self):
        buttons = {}
        names = list(self.settings.difficulty_profiles.keys())
        colors = [(0, 150, 60), (0, 110, 190), (180, 60, 60)]
        count = len(names)
        total_width = count * 240 + (count - 1) * 24
        start_x = (self.settings.screen_width - total_width) // 2
        y = self.settings.screen_height // 2 + 60

        for index, name in enumerate(names):
            center = (start_x + index * (240 + 24) + 120, y)
            color = colors[index % len(colors)]
            buttons[name] = Button(self, name, center=center, width=240, height=70, color=color)

        return buttons


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
