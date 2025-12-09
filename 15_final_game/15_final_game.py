"""Final Alien Invasion game with music, scoring, and multiple levels.

Run this module to launch the game window::

    python3 assignments/15_final_game/15_final_game.py

Use the arrow keys to move, Space to fire, and Q to quit.
"""

import sys
from pathlib import Path
from random import choice, random
from typing import Dict, Optional, Tuple

import pygame
from pygame.sprite import Sprite

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
MUSIC_PATH = ASSETS_DIR / "techno.mp3"
LASER_SOUND_PATH = ASSETS_DIR / "laser_shot.wav"
EXPLOSION_SOUND_PATH = ASSETS_DIR / "alien_explosion.wav"
HIGH_SCORE_PATH = PROJECT_ROOT / "alien_invasion_high_score.txt"


class Settings:
    """Store settings for Alien Invasion and handle level scaling."""
    
    def __init__(self) -> None:
        # Screen setup
        self.screen_width = 1200
        self.screen_height = 800

        # Ship setup
        self.ship_limit = 3

        # Bullets
        self.bullet_width = 4
        self.bullet_height = 16
        self.bullet_color = (255, 215, 160)
        self.alien_bullet_width = 4
        self.alien_bullet_height = 18
        self.alien_bullet_color = (255, 120, 150)
        self.alien_bullet_speed = 3.0
        self.alien_fire_delay = 1500

        # Aliens
        self.alien_size = (48, 40)

        # Power-ups
        self.powerup_speed = 1.7
        self.powerup_duration = 6500
        self.powerup_drop_chance = 0.15
        self.powerup_color = (255, 215, 0)

        # Difficulty accelerators
        self.speedup_scale = 1.12
        self.score_scale = 1.4

        # Visual palette recycled each level
        self.bg_palette = [
            (5, 5, 35),
            (10, 10, 55),
            (25, 5, 45),
            (5, 30, 50),
        ]
        self.alien_palette = [
            (70, 210, 255),
            (255, 125, 125),
            (120, 240, 170),
            (255, 215, 0),
        ]
        self.ship_color = (240, 240, 240)
        self.hud_color = (245, 245, 245)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        self.ship_speed = 3.0
        self.bullet_speed = 5.0
        self.alien_bullet_speed = 3.0
        self.alien_speed = 0.8
        self.fleet_drop_speed = 12
        self.fleet_direction = 1
        self.bullets_allowed = 4
        self.alien_points = 50
        self.alien_fire_delay = 1500

    def increase_speed(self) -> None:
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed = int(self.fleet_drop_speed * 1.05)
        self.alien_points = int(self.alien_points * self.score_scale)
        self.alien_fire_delay = max(500, int(self.alien_fire_delay * 0.95))

    def get_background_color(self, level: int) -> Tuple[int, int, int]:
        return self.bg_palette[(level - 1) % len(self.bg_palette)]

    def get_alien_color(self, level: int) -> Tuple[int, int, int]:
        return self.alien_palette[(level - 1) % len(self.alien_palette)]


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        self.settings = ai_game.settings
        self.high_score_path = HIGH_SCORE_PATH
        self.reset_stats()
        self.game_active = False
        self.high_score = self._load_high_score()

    def reset_stats(self) -> None:
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self) -> int:
        try:
            return int(self.high_score_path.read_text().strip())
        except (OSError, ValueError):
            return 0

    def save_high_score(self) -> None:
        try:
            self.high_score_path.write_text(str(self.high_score))
        except OSError:
            pass


class Ship:
    """Ship that moves horizontally along the bottom of the screen."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.width = 80
        self.height = 48
        self.color = self.settings.ship_color

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self) -> None:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self) -> None:
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(
            self.screen,
            (120, 200, 255),
            (self.rect.x + 12, self.rect.y + 10, self.width - 24, 10),
            border_radius=5,
        )


class Bullet(Sprite):
    """Bullet fired from the ship."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=3)


class AlienBullet(Sprite):
    """Projectile that aliens fire toward the player."""

    def __init__(self, ai_game: "AlienInvasion", alien: "Alien") -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)
        self.rect.midtop = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_laser(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=3)


class PowerUp(Sprite):
    """Falling booster that grants unlimited fire temporarily."""

    def __init__(self, ai_game: "AlienInvasion", center: Tuple[int, int]) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.powerup_color
        self.rect = pygame.Rect(0, 0, 28, 28)
        self.rect.center = center
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y += self.settings.powerup_speed
        self.rect.y = self.y

    def draw(self) -> None:
        pygame.draw.rect(self.screen, (30, 30, 30), self.rect, border_radius=10)
        inner_rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(self.screen, self.color, inner_rect, border_radius=8)


class Alien(Sprite):
    """An alien in the invading fleet."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        width, height = self.settings.alien_size
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = width
        self.rect.y = height
        self.x = float(self.rect.x)

        self._paint()

    def _paint(self) -> None:
        color = self.settings.get_alien_color(self.stats.level)
        width, height = self.settings.alien_size
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, color, (0, 0, width, height), border_radius=6)
        pygame.draw.circle(self.image, (255, 255, 255), (width // 3, height // 3), 6)
        pygame.draw.circle(self.image, (255, 255, 255), (2 * width // 3, height // 3), 6)
        pygame.draw.rect(self.image, (0, 0, 0), (width // 3 - 2, height // 3 - 2, 6, 4))

    def update(self) -> None:
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self) -> bool:
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0


class Scoreboard:
    """Display scoring information."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = self.settings.hud_color
        self.font_small = pygame.font.SysFont(None, 32)
        self.font_large = pygame.font.SysFont(None, 40)

        self.prep_images()

    def prep_images(self) -> None:
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self) -> None:
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font_large.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 20
        self.score_rect.top = 20

    def prep_high_score(self) -> None:
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font_large.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self) -> None:
        level_str = f"Level {self.stats.level}"
        self.level_image = self.font_large.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = 20
        self.level_rect.top = self.score_rect.bottom + 8

    def prep_ships(self) -> None:
        ships_str = f"Ships: {self.stats.ships_left}"
        self.ships_image = self.font_small.render(ships_str, True, self.text_color)
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.left = 20
        self.ships_rect.top = self.level_rect.bottom + 8

    def show_score(self) -> None:
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)

    def draw_powerup_status(self, message: str) -> None:
        info_image = self.font_small.render(message, True, self.text_color)
        info_rect = info_image.get_rect()
        info_rect.topright = (self.screen_rect.right - 20, 20)
        self.screen.blit(info_image, info_rect)

    def check_high_score(self) -> None:
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats.save_high_score()
            self.prep_high_score()


class Button:
    """Simple Play button."""

    def __init__(self, ai_game: "AlienInvasion", msg: str) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 320, 70
        self.button_color = (0, 170, 120)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class MusicController:
    """Load and play background music safely."""

    def __init__(self, music_path: Path) -> None:
        self.music_path = music_path
        self.available = False
        self.playing = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return

        if self.music_path.exists():
            try:
                pygame.mixer.music.load(self.music_path)
            except pygame.error:
                return
            self.available = True

    def play_loop(self) -> None:
        if self.available:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            self.playing = True

    def fadeout(self, ms: int = 400) -> None:
        if self.available and self.playing:
            pygame.mixer.music.fadeout(ms)
            self.playing = False


class SoundEffects:
    """Simple wrapper for playing short sound effects."""

    def __init__(self, laser_path: Path, explosion_path: Path) -> None:
        self.laser_path = laser_path
        self.explosion_path = explosion_path
        self.laser_sound: Optional[pygame.mixer.Sound] = None
        self.explosion_sound: Optional[pygame.mixer.Sound] = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return

        if self.laser_path.exists():
            try:
                self.laser_sound = pygame.mixer.Sound(str(self.laser_path))
                self.laser_sound.set_volume(0.5)
            except pygame.error:
                self.laser_sound = None

        if self.explosion_path.exists():
            try:
                self.explosion_sound = pygame.mixer.Sound(str(self.explosion_path))
                self.explosion_sound.set_volume(0.6)
            except pygame.error:
                self.explosion_sound = None

    def play_laser(self) -> None:
        if self.laser_sound:
            self.laser_sound.play()

    def play_explosion(self) -> None:
        if self.explosion_sound:
            self.explosion_sound.play()


class AlienInvasion:
    """Overall game controller."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.clock = pygame.time.Clock()

        self.high_score_path = HIGH_SCORE_PATH

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.play_button = Button(self, "Play Alien Invasion")

        self.music = MusicController(MUSIC_PATH)
        self.music.play_loop()
        self.sounds = SoundEffects(LASER_SOUND_PATH, EXPLOSION_SOUND_PATH)

        self.level_overlay: Dict[str, int | pygame.Surface | pygame.Rect] = {
            "surface": None,
            "rect": None,
            "expires": 0,
        }
        self.next_alien_shot = 0
        self.unlimited_until = 0

    def run_game(self) -> None:
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
                self._update_powerups()

            self._update_screen()
            self.clock.tick(60)

    # Event handling -----------------------------------------------------

    def _check_events(self) -> None:
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

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos: Tuple[int, int]) -> None:
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _quit_game(self) -> None:
        if self.stats.high_score > 0:
            self.stats.save_high_score()
        pygame.quit()
        sys.exit()

    # Game state transitions --------------------------------------------

    def _start_game(self) -> None:
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.powerups.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.unlimited_until = 0
        self._schedule_next_alien_shot()

        pygame.mouse.set_visible(False)
        self._announce_level()

    def _announce_level(self) -> None:
        overlay_font = pygame.font.SysFont(None, 64)
        text = f"Level {self.stats.level}"
        surface = overlay_font.render(text, True, (255, 255, 255))
        surface.set_alpha(220)
        rect = surface.get_rect()
        rect.center = (self.settings.screen_width // 2, 120)
        self.level_overlay = {"surface": surface, "rect": rect, "expires": pygame.time.get_ticks() + 2000}

    def _schedule_next_alien_shot(self) -> None:
        base_delay = self.settings.alien_fire_delay
        jitter = int(base_delay * 0.5 * random())
        self.next_alien_shot = pygame.time.get_ticks() + base_delay + jitter

    def _player_has_unlimited_fire(self) -> bool:
        return pygame.time.get_ticks() < self.unlimited_until

    def _activate_unlimited_fire(self) -> None:
        self.unlimited_until = pygame.time.get_ticks() + self.settings.powerup_duration

    def _powerup_status_text(self) -> str:
        if not self.stats.game_active:
            return "Power-Up: Press Play"
        if self._player_has_unlimited_fire():
            remaining = max(0, (self.unlimited_until - pygame.time.get_ticks()) // 1000)
            return f"Power-Up: UNLIMITED ({remaining}s)"
        return "Power-Up: Shoot foes for boosts"

    def _maybe_drop_powerup(self, center: Tuple[int, int]) -> None:
        if random() < self.settings.powerup_drop_chance:
            self.powerups.add(PowerUp(self, center))

    def _finish_level(self) -> None:
        self.bullets.empty()
        self.alien_bullets.empty()
        self.powerups.empty()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()
        self._create_fleet()
        self._announce_level()
        self._schedule_next_alien_shot()

    # Bullets ------------------------------------------------------------

    def _fire_bullet(self) -> None:
        if not self.stats.game_active:
            return
        has_capacity = len(self.bullets) < self.settings.bullets_allowed
        if self._player_has_unlimited_fire() or has_capacity:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.play_laser()

    def _update_bullets(self) -> None:
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    self._maybe_drop_powerup(alien.rect.center)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sounds.play_explosion()

        if not self.aliens:
            self._finish_level()

    def _update_alien_bullets(self) -> None:
        self.alien_bullets.update()
        ship_hit = False
        for laser in self.alien_bullets.copy():
            if laser.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(laser)
                continue
            if laser.rect.colliderect(self.ship.rect):
                self.alien_bullets.remove(laser)
                ship_hit = True
        if ship_hit:
            self._ship_hit()

    def _update_powerups(self) -> None:
        self.powerups.update()
        collected = False
        for powerup in self.powerups.copy():
            if powerup.rect.top >= self.settings.screen_height:
                self.powerups.remove(powerup)
                continue
            if powerup.rect.colliderect(self.ship.rect):
                self.powerups.remove(powerup)
                collected = True
        if collected:
            self._activate_unlimited_fire()

    # Aliens -------------------------------------------------------------

    def _create_fleet(self) -> None:
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (1.5 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = max(2, int(available_space_y // (1.5 * alien_height)))

        for row_number in range(int(number_rows)):
            for alien_number in range(int(number_aliens_x)):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number: int, row_number: int, alien_width: int, alien_height: int) -> None:
        alien = Alien(self)
        alien.x = alien_width + alien_number * alien_width * 1.5
        alien.rect.x = alien.x
        alien.rect.y = alien_height + row_number * alien_height * 1.5
        self.aliens.add(alien)

    def _try_alien_shot(self) -> None:
        if not self.aliens:
            return
        if pygame.time.get_ticks() >= self.next_alien_shot:
            shooter = choice(self.aliens.sprites())
            self.alien_bullets.add(AlienBullet(self, shooter))
            self._schedule_next_alien_shot()

    def _update_aliens(self) -> None:
        self._check_fleet_edges()
        self.aliens.update()
        self._try_alien_shot()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self) -> None:
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self) -> None:
        self.unlimited_until = 0
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.powerups.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.time.delay(600)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.level_overlay = {"surface": None, "rect": None, "expires": 0}
        self.sounds.play_explosion()
        self._schedule_next_alien_shot()

    def _check_aliens_bottom(self) -> None:
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # Drawing ------------------------------------------------------------

    def _update_screen(self) -> None:
        level_for_color = max(1, self.stats.level)
        bg_color = self.settings.get_background_color(level_for_color)
        self.screen.fill(bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for laser in self.alien_bullets.sprites():
            laser.draw_laser()
        for powerup in self.powerups.sprites():
            powerup.draw()
        self.ship.draw()
        self.aliens.draw(self.screen)

        self.sb.show_score()
        self.sb.draw_powerup_status(self._powerup_status_text())
        self._draw_level_overlay()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _draw_level_overlay(self) -> None:
        surface = self.level_overlay.get("surface")
        rect = self.level_overlay.get("rect")
        expires = self.level_overlay.get("expires", 0)
        if surface and rect and pygame.time.get_ticks() < expires:
            overlay_bg = pygame.Surface((rect.width + 40, rect.height + 20), pygame.SRCALPHA)
            overlay_bg.fill((0, 0, 0, 140))
            bg_rect = overlay_bg.get_rect()
            bg_rect.center = rect.center
            self.screen.blit(overlay_bg, bg_rect)
            self.screen.blit(surface, rect)


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
