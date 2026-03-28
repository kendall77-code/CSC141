import io
import math
import random
import struct
import sys
import wave

import pygame


pygame.init()
pygame.mixer.init()


# window setup
screen_width = 640
screen_height = 480
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball Click Game")
clock = pygame.time.Clock()


# colors
WHITE = (255, 255, 255)
RED = (220, 40, 40)
BLACK = (0, 0, 0)




def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)



def create_success_sound():
    sample_rate = 44100
    duration = 0.15
    frequency = 880
    volume = 0.35
    num_samples = int(sample_rate * duration)

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in range(num_samples):
            sine_value = math.sin(2 * math.pi * frequency * (sample / sample_rate))
            amplitude = int(32767 * volume * sine_value)
            wav_file.writeframes(struct.pack("<h", amplitude))

    wav_buffer.seek(0)
    return pygame.mixer.Sound(file=wav_buffer)


success_sound = create_success_sound()



ball_radius = 25
ball_x = random.randint(ball_radius, screen_width - ball_radius * 2)
ball_y = random.randint(ball_radius, screen_height - ball_radius * 2)
ball_rect = pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2)

x_speed = 3
y_speed = -3



score = 0
goal_score = 5
start_time = pygame.time.get_ticks()
finish_time = None
game_over = False


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if ball_rect.collidepoint(mouse_x, mouse_y):
                score += 1
                success_sound.play()

                # reset ball location
                ball_x = random.randint(0, screen_width - ball_radius * 2)
                ball_y = random.randint(0, screen_height - ball_radius * 2)

                # increase absolute speed values by 1 to 5
                x_speed = abs(x_speed) + random.randint(1, 5)
                y_speed = abs(y_speed) + random.randint(1, 5)

                if score >= goal_score:
                    game_over = True
                    finish_time = pygame.time.get_ticks()

    if not game_over:
        # move the ball
        ball_x += x_speed
        ball_y += y_speed

        # bounce on walls
        if ball_x <= 0 or ball_x + ball_radius * 2 >= screen_width:
            x_speed = -x_speed

        if ball_y <= 0 or ball_y + ball_radius * 2 >= screen_height:
            y_speed = -y_speed

        # keep rect updated for click detection
        ball_rect.x = ball_x
        ball_rect.y = ball_y

    window.fill(WHITE)

    # draw game objects
    if not game_over:
        pygame.draw.circle(
            window,
            RED,
            (ball_x + ball_radius, ball_y + ball_radius),
            ball_radius,
        )

    draw_text(window, f"Score: {score}", 10, 10, BLACK, 30)

    if game_over:
        total_seconds = (finish_time - start_time) / 1000
        message = f"You finished in {total_seconds:.2f} seconds!"
        message_surface = pygame.font.SysFont(None, 42).render(message, True, BLACK)
        message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        window.blit(message_surface, message_rect)

    pygame.display.update()


pygame.quit()
sys.exit()
