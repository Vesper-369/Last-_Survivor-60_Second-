from importlib.resources import path

import pygame

class Player:
    def __init__(self):
        # Animation frames (FIXED INDENTATION + SAFE LOADING)
        try:
            def load_image(path):
                img = pygame.image.load(path).convert_alpha()
                img.set_colorkey((255, 255, 255))  # remove white background
                return pygame.transform.scale(img, (60, 60))

            self.frames = [
                load_image("assets/player1.png"),
                load_image("assets/player2.png")
            ]

        except:
            # fallback if image not found
            temp = pygame.Surface((60, 60))
            temp.fill((0, 255, 0))
            self.frames = [temp, temp]

        self.frame_index = 0
        self.animation_speed = 0.1

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(400, 300))

        self.speed = 5
        self.health = 100

    def move(self, keys):
        moving = False

        if keys[pygame.K_LEFT or pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT or pygame.K_d]:
            self.rect.x += self.speed
            moving = True
        if keys[pygame.K_UP or pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN or pygame.K_s]:
            self.rect.y += self.speed
            moving = True

        # Animation update
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

        # Screen bounds (FIXED HARD-CODE ISSUE)
        from utils import WIDTH, HEIGHT

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)