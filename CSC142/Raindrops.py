import random
import sys

import pygame


class Raindrop:
    __slots__ = ["x", "y", "radius"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1

    def draw(self, window):
        pygame.draw.circle(window, (0, 0, 255), (self.x, self.y), self.radius)

    def update(self):
        self.radius += 1


class RaindropsManager:
    RAIN_RATE = 400
    MAX_RADIUS = 60

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Raindrops")
        self.clock = pygame.time.Clock()
        self.raindrops = []
        self.last_drop_time = pygame.time.get_ticks()
        self.running = True

    def add_raindrop(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        self.raindrops.append(Raindrop(x, y))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_raindrops(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_drop_time >= self.RAIN_RATE:
            self.add_raindrop()
            self.last_drop_time = current_time

        for raindrop in self.raindrops:
            raindrop.update()

        self.raindrops = [
            raindrop for raindrop in self.raindrops
            if raindrop.radius <= self.MAX_RADIUS
        ]

    def draw(self):
        self.window.fill((230, 230, 230))

        for raindrop in self.raindrops:
            raindrop.draw(self.window)

        pygame.display.update()

    def run(self):
        while self.running:
            self.check_events()
            self.update_raindrops()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


manager = RaindropsManager()
manager.run()
