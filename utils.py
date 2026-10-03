import random
import pygame

WIDTH, HEIGHT = 1200, 800

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        return random.randint(0, WIDTH), 0
    elif side == "bottom":
        return random.randint(0, WIDTH), HEIGHT
    elif side == "left":
        return 0, random.randint(0, HEIGHT)
    else:
        return WIDTH, random.randint(0, HEIGHT)


def draw_text(screen, text, size, x, y, center=False, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    screen.blit(text_surface, (x, y))