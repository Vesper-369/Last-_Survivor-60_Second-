import pygame
import sys
import time
import random
from player import Player
from enemy import Enemy
from utils import spawn_enemy, draw_text, WIDTH, HEIGHT

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Survivor: 60 Seconds")

clock = pygame.time.Clock()

# Load background
bg = pygame.transform.scale(
    pygame.image.load("assets/bg.png").convert(),
    (WIDTH, HEIGHT)
)

player = Player()
enemies = []

start_time = time.time()
spawn_timer = 0

# Screen shake variable
shake = 0
fullscreen = False
TIMER_SPEED = 0.8

running = True

while running:
    dt = clock.tick(60) / 1000

    elapsed = time.time() - start_time
    time_left = max(0, 60 - int(elapsed * TIMER_SPEED))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_f, pygame.K_F11):
                fullscreen = not fullscreen
                flags = pygame.FULLSCREEN if fullscreen else 0
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Spawn enemies (faster over time)
    spawn_timer += 1
    if spawn_timer > max(30, 60 - int(elapsed)):
        x, y = spawn_enemy()
        enemies.append(Enemy(x, y))
        spawn_timer = 0

    if len(enemies) > 35:  # Limit max enemies
        enemies = enemies[-35:]

    # Move enemies
    for enemy in enemies[:]:
        enemy.move_towards_player(player)

        if player.rect.colliderect(enemy.rect):
            player.health -= 2
            shake = 10   # 🔥 trigger screen shake
            enemies.remove(enemy)

    # 🔥 SCREEN SHAKE EFFECT
    offset_x, offset_y = 0, 0
    if shake > 0:
        offset_x = random.randint(-shake, shake)
        offset_y = random.randint(-shake, shake)
        shake -= 1

    # DRAW
    screen.blit(bg, (offset_x, offset_y))

    # Draw player & enemies
    screen.blit(player.image, (player.rect.x + offset_x, player.rect.y + offset_y))

    for enemy in enemies:
        screen.blit(enemy.image, (enemy.rect.x + offset_x, enemy.rect.y + offset_y))

    # 🔥 Player glow effect
    pygame.draw.circle(
        screen,
        (0, 255, 0),
        (player.rect.centerx + offset_x, player.rect.centery + offset_y),
        35,
        2
    )

    # UI
    draw_text(screen, f"Time: {time_left}", 30, 10, 10)
    draw_text(screen, f"Health: {player.health}", 30, 10, 40)

    # GAME OVER
    if player.health <= 0:
        draw_text(screen, "GAME OVER", 100, WIDTH // 2, HEIGHT // 2, center=True, color=(255, 0, 0)) 
        font = pygame.font.SysFont(None, 50)
        color = (255, 0, 0) if time_left > 0 else (0, 255, 0)
        text_surface = font.render(f"Time Survived: {60 - time_left}s", True, color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # WIN
    if time_left <= 0:
        draw_text(screen, "YOU SURVIVED!", 100, WIDTH // 2, HEIGHT // 2, center=True, color=(0, 255, 0))
        font = pygame.font.SysFont(None, 50)
        color = (0, 255, 0) if player.health > 50 else (255, 0, 0)
        text_surface = font.render(f"Health: {player.health}", True, color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()