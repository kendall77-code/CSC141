import math
import random
import sys
from pathlib import Path

import pygame
from pygame.sprite import Sprite


class Settings:
    """Store all settings for Sideways Shooter."""

    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (5, 10, 25)

        # Ship settings
        self.ship_limit = 3
        self.ship_speed_default = 3.0
        self.ship_boost_speed = 5.2

        # Bullet settings
        self.bullet_speed_default = 6.0
        self.bullet_width = 16
        self.bullet_height = 4
        self.bullet_color = (255, 220, 60)
        self.bullets_allowed_default = 5

        # Alien settings
        self.alien_speed_default = 1.8
        self.alien_color = (90, 200, 255)
        self.alien_points_default = 40

        # Starfield customization
        self.star_count = 80
        self.star_colors = [(80, 80, 140), (140, 140, 220), (120, 90, 180)]
        self.star_speeds = (0.3, 0.6, 0.9)

        # Difficulty scaling
        self.speedup_scale = 1.15
        self.score_scale = 1.4

        self.reset_dynamic_settings()

    def reset_dynamic_settings(self):
        self.ship_speed = self.ship_speed_default
        self.bullet_speed = self.bullet_speed_default
        self.alien_speed = self.alien_speed_default
        self.bullets_allowed = self.bullets_allowed_default
        self.alien_points = self.alien_points_default

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


class GameStats:
    """Track statistics for Sideways Shooter."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.high_score_file = Path("sideways_high_score.txt")
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
    """Player ship hugging the left boundary."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.width = 80
        self.height = 32
        self.color = (60, 230, 140)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)
        self.boosting = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        speed = self.settings.ship_speed
        if self.boosting:
            speed = self.settings.ship_boost_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += speed
        self.rect.y = self.y

    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=8)


class Bullet(Sprite):
    """Bullet fired from the ship moving to the right."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midleft = ai_game.ship.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)


class Alien(Sprite):
    """Alien craft drifting in from the right."""

    def __init__(self, ai_game, position):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_color

        self.width = 50
        self.height = 34
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x, self.rect.y = position
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

        self.vertical_range = random.randint(12, 28)
        self.vertical_direction = random.choice([-1, 1])
        self.vertical_speed = random.uniform(0.4, 0.9)
        self.base_y = float(self.rect.y)
        self.wave_phase = random.uniform(0, math.pi)

    def update(self):
        self.float_x -= self.settings.alien_speed
        self.rect.x = self.float_x

        # Bob vertically for some life
        self.wave_phase += 0.04
        self.float_y = self.base_y + math.sin(self.wave_phase) * self.vertical_range
        self.rect.y = int(self.float_y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(self.rect.x + 8, self.rect.y + 10, 10, 4),
            border_radius=2,
        )


class Star(Sprite):
    """Background star for subtle motion."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.speed = random.choice(self.settings.star_speeds)
        self.color = random.choice(self.settings.star_colors)

        self.rect = pygame.Rect(0, 0, random.randint(1, 3), random.randint(1, 3))
        self.x = float(random.randint(0, self.settings.screen_width))
        self.y = float(random.randint(0, self.settings.screen_height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        self.x -= self.speed
        if self.x + self.rect.width < 0:
            self.x = float(self.settings.screen_width)
            self.y = float(random.randint(0, self.settings.screen_height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw_star(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Button:
    """Clickable button such as Play."""

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 240, 70
        self.button_color = (0, 180, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)


class Scoreboard:
    """Display scoring information."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 36)

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        score_str = f"Score: {self.stats.score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = f"Record: {self.stats.high_score:,}"
        self.high_score_image = self.font.render(high_score, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        level_str = f"Wave: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 8

    def prep_ships(self):
        ships_str = f"Ships: {self.stats.ships_left}"
        self.ships_image = self.font.render(ships_str, True, self.text_color, self.settings.bg_color)
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.left = 20
        self.ships_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)


class SidewaysShooter:
    """Game controller class."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Sideways Shooter — Final")

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.play_button = Button(self, "Play")
        self._create_starfield()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.stars.update()
            else:
                self.stars.update()
            self._update_screen()

    # --- Setup helpers ---

    def _create_starfield(self):
        for _ in range(self.settings.star_count):
            self.stars.add(Star(self))

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
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_LSHIFT:
            self.ship.boosting = True
        elif event.key == pygame.K_q:
            self._quit_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_LSHIFT:
            self.ship.boosting = False

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.reset_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_images()

        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self._create_wave()

        pygame.mouse.set_visible(False)

    def _quit_game(self):
        self.stats.save_high_score()
        pygame.quit()
        sys.exit()

    # --- Update loops ---

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        self.bullets.update()
        for bullet in list(self.bullets):
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)
            self.scoreboard.prep_score()
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
                self.stats.save_high_score()
                self.scoreboard.prep_high_score()

        if not self.aliens:
            self._start_new_wave()

    def _start_new_wave(self):
        self.settings.increase_speed()
        self.stats.level += 1
        self.scoreboard.prep_level()
        self.bullets.empty()
        self._create_wave()

    def _create_wave(self):
        alien = Alien(self, (0, 0))
        alien_width, alien_height = alien.rect.size
        margin_right = 40
        available_space_x = self.settings.screen_width - (self.ship.rect.width + 200)
        columns = max(2, available_space_x // (alien_width + 35))
        start_x = self.settings.screen_width - margin_right - alien_width

        available_space_y = self.settings.screen_height - 2 * alien_height
        rows = max(2, available_space_y // (alien_height + 20))

        for col in range(columns):
            for row in range(rows):
                x = start_x - col * (alien_width + 35)
                y = alien_height + row * (alien_height + 18)
                if x > self.ship.rect.width + 120:
                    self.aliens.add(Alien(self, (x, y)))

    def _update_aliens(self):
        self.aliens.update()
        for alien in self.aliens.copy():
            if alien.rect.right < 0:
                self.aliens.remove(alien)
                self._ship_hit()
                break

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self.bullets.empty()
            self.aliens.empty()
            self._create_wave()
            self.ship.center_ship()
            pygame.time.delay(300)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.save_high_score()

    # --- Drawing ---

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for star in self.stars.sprites():
            star.draw_star()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.draw()
        self.ship.draw()

        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    game = SidewaysShooter()
    game.run_game()
