import sys
import pygame


class Rocket:
    """A rocket that can move around the screen."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Load rocket image
        self.image = pygame.image.load("images/rocket.bmp")
        self.rect = self.image.get_rect()

        # Start rocket at the center of the screen
        self.rect.center = self.screen_rect.center

        # Store decimal values for rocket's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Speed
        self.speed = 1.5

    def update(self):
        """Update rocket position based on movement flags."""
        
        # Move right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.speed
        
        # Move left
        if self.moving_left and self.rect.left > 0:
            self.x -= self.speed
        
        # Move up
        if self.moving_up and self.rect.top > 0:
            self.y -= self.speed
        
        # Move down
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.speed

        # Update rect from decimal values
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the rocket at its current position."""
        self.screen.blit(self.image, self.rect)


def run_game():
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rocket Control")

    rocket = Rocket(screen)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keydown
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rocket.moving_right = True
                elif event.key == pygame.K_LEFT:
                    rocket.moving_left = True
                elif event.key == pygame.K_UP:
                    rocket.moving_up = True
                elif event.key == pygame.K_DOWN:
                    rocket.moving_down = True

            # Keyup
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    rocket.moving_right = False
                elif event.key == pygame.K_LEFT:
                    rocket.moving_left = False
                elif event.key == pygame.K_UP:
                    rocket.moving_up = False
                elif event.key == pygame.K_DOWN:
                    rocket.moving_down = False

        # Update and redraw screen
        rocket.update()
        screen.fill((30, 30, 30))  # dark background
        rocket.blitme()

        pygame.display.flip()


if __name__ == "__main__":
    run_game()

        # Your game code here
        # ...

    input("Press Enter to close the game...")
