from sys import path

import pygame
import math

class Enemy:
    def __init__(self, x, y):
        def load_image(path):
            img = pygame.image.load(path).convert_alpha()
            img.set_colorkey((255, 255, 255))  # remove white background
            return pygame.transform.scale(img, (50, 50))

        self.frames = [
            load_image("assets/enemy1.png"),
            load_image("assets/enemy2.png")
        ]

        self.frame_index = 0
        self.animation_speed = 0.08

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 2

    def move_towards_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        dx /= dist
        dy /= dist

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Animate
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)