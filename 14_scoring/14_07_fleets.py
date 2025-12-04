import random
import sys
from pathlib import Path

import pygame
from pygame.sprite import Sprite


class Settings:
    """Store all settings for Alien Invasion."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 30)

        self.ship_limit = 3
        self.ship_speed_default = 2.8
        self.ship_color = (240, 240, 240)

        self.bullet_speed_default = 4.5
        self.bullet_width = 4
        self.bullet_height = 18
        self.bullet_color = (255, 200, 50)
        self.bullets_allowed_default = 4

        self.alien_speed_default = 0.9
        self.fleet_drop_speed_default = 8
        self.alien_color = (80, 200, 255)

        self.alien_points_default = 50

        self.speedup_scale = 1.1
        self.score_scale = 1.4

        self.alien_bullet_speed_default = 2.5
        self.alien_bullet_color = (255, 120, 120)
        self.alien_bullets_allowed = 6
        self.alien_fire_chance_default = 0.008
        self.max_alien_fire_chance = 0.05

        self.reset_dynamic_settings()

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.alien_bullet_speed *= self.speedup_scale
        self.alien_fire_chance = min(
            self.max_alien_fire_chance, self.alien_fire_chance * 1.15
        )

    def reset_dynamic_settings(self):
        """Return speeds/scoring to their defaults when the game restarts."""
        self.ship_speed = self.ship_speed_default
        self.bullet_speed = self.bullet_speed_default
        self.alien_speed = self.alien_speed_default
        self.fleet_drop_speed = self.fleet_drop_speed_default
        self.fleet_direction = 1
        self.bullets_allowed = self.bullets_allowed_default
        self.alien_points = self.alien_points_default
        self.alien_bullet_speed = self.alien_bullet_speed_default
        self.alien_fire_chance = self.alien_fire_chance_default


class GameStats:
    """Track game statistics and store persistent high score."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.high_score_file = Path("high_score.txt")
        self.reset_stats()
        self.game_active = False
        self.high_score = self._load_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        if self.high_score_file.exists():
            try:
                return int(self.high_score_file.read_text().strip() or 0)
            except ValueError:
                return 0
        return 0

    def save_high_score(self):
        self.high_score_file.write_text(str(self.high_score))


class Ship:
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


class AlienBullet(Sprite):
    """Bullets fired downward by aliens."""

    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.alien_bullet_color, self.rect)


class Alien(Sprite):
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
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 220, 60
        self.button_color = (0, 180, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Scoreboard:
    """Report scoring information."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 40)

        self.prep_images()

    def prep_images(self):
        """Render all score-related images at once."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        score_str = f"Score: {self.stats.score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_game.settings.bg_color
        )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score_str = f"High Score: {self.stats.high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_game.settings.bg_color
        )
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.ai_game.settings.bg_color
        )
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        ships_str = f"Ships: {self.stats.ships_left}"
        self.ships_image = self.font.render(
            ships_str, True, self.text_color, self.ai_game.settings.bg_color
        )
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.left = 20
        self.ships_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion — High Score")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
            self._update_screen()

    # --- Event handling ---

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._quit_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.reset_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_images()

        self.bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _quit_game(self):
        self.stats.save_high_score()
        pygame.quit()
        sys.exit()

    # --- Bullets ---

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in list(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for bullet in list(self.alien_bullets):
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self.alien_bullets.empty()
            self._ship_hit()

        pygame.sprite.groupcollide(self.bullets, self.alien_bullets, True, True)

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)
            self.scoreboard.prep_score()
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
                self.stats.save_high_score()
                self.scoreboard.prep_high_score()

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Begin a new level with a fresh fleet and faster pace."""
        self.bullets.empty()
        self.alien_bullets.empty()
        self.settings.increase_speed()
        self.stats.level += 1
        self.scoreboard.prep_level()
        self._create_fleet()

    # --- Alien bullets ---

    def _maybe_fire_alien_bullet(self):
        if not self.aliens or len(self.alien_bullets) >= self.settings.alien_bullets_allowed:
            return
        if random.random() < self.settings.alien_fire_chance:
            shooter = random.choice(self.aliens.sprites())
            self._fire_alien_bullet(shooter)

    def _fire_alien_bullet(self, alien):
        bullet = AlienBullet(self, alien)
        self.alien_bullets.add(bullet)

    # --- Aliens ---

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = max(1, available_space_y // (2 * alien_height))

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(
                    alien_number, row_number, alien_width, alien_height
                )

    def _create_alien(
        self, alien_number, row_number, alien_width, alien_height
    ):
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._maybe_fire_alien_bullet()

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
            self.scoreboard.prep_ships()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.time.delay(500)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.save_high_score()
            self.scoreboard.prep_high_score()

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
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        self.ship.draw()
        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
