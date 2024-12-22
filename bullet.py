import pygame
import sys

def move_bullets(bullets, BULLET_SPEED, WIDTH):
    return [(x + BULLET_SPEED, y) for x, y in bullets if x < WIDTH]  # Keep bullets on-screen

def draw_bullets(bullets, BULLET_COLOR, BULLET_RADIUS, screen):
    for x, y in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (x, y), BULLET_RADIUS)

def move_bullets(bullets, BULLET_SPEED, WIDTH):
    return [(x + BULLET_SPEED, y) for x, y in bullets if x < WIDTH]  # Keep bullets on-screen

def draw_bullets(bullets, BULLET_COLOR, BULLET_RADIUS, screen):
    for x, y in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (x, y), BULLET_RADIUS)

def check_bullet_collisions(bullets, pipes, BULLET_RADIUS):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0] - BULLET_RADIUS, bullet[1] - BULLET_RADIUS, BULLET_RADIUS * 2, BULLET_RADIUS * 2)
        for pipe in pipes[:]:
            if bullet_rect.colliderect(pipe):
                bullets.remove(bullet)
                break

def check_bullet_enemy_collisions(bullets, enemies, BULLET_RADIUS, score):
    for bullet in bullets[:]:  # Iterate through a copy of the list
        for enemy in enemies[:]:
            if pygame.Rect(bullet[0] - BULLET_RADIUS, bullet[1] - BULLET_RADIUS, BULLET_RADIUS * 2, BULLET_RADIUS * 2).colliderect(enemy):
                score += 20
                bullets.remove(bullet)
                enemies.remove(enemy)
                break