import pygame
import sys
import random
import math

def background_animation(screen, background_images, scroll_positions, scroll_speeds, game_active) :
    screen_width, screen_height = screen.get_size()

    for i, image in enumerate(background_images):

        scaled_background = pygame.transform.scale(image, (screen_width, screen_height))
        if game_active == True:
            scroll_positions[i] -= scroll_speeds[i]
        if scroll_positions[i] <= -screen_width:
            scroll_positions[i] = 0

        screen.blit(scaled_background, (scroll_positions[i], 0))
        screen.blit(scaled_background, (scroll_positions[i] + screen_width, 0))

def create_pipe(HEIGHT, WIDTH, PIPE_GAP, PIPE_WIDTH):
    height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP)
    return top_pipe, bottom_pipe

def move_pipes(pipes, PIPE_SPEED):
    for pipe in pipes:
        pipe.x -= PIPE_SPEED
    return [pipe for pipe in pipes if pipe.right > 0]   #Keeps pipes on-screen

def draw_pipes(pipes, PIPE_COLOR, screen):
    for pipe in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, pipe)

def spawn_enemy(pipe, PIPE_WIDTH, ENEMY_WIDTH, ENEMY_HEIGHT, PIPE_GAP):
    x = pipe.x + PIPE_WIDTH // 2 - ENEMY_WIDTH // 2
    y = pipe.height + PIPE_GAP // 2 - ENEMY_HEIGHT // 2
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

def move_enemies(enemies, ENEMY_SPEED, enemy_amplitude):
    for enemy in enemies:
        enemy.x -= ENEMY_SPEED
        enemy.y = enemy.y + math.sin(enemy.x * 0.045) * enemy_amplitude
    return [enemy for enemy in enemies if enemy.right > 0]

def draw_enemies(enemies, enemy_index, enemy_animation_resized, screen):
    for enemy in enemies:
        E_current_frame = enemy_animation_resized[enemy_index]
        screen.blit(E_current_frame, enemy)

def check_collision(pipes, enemies, bird, HEIGHT):
    for pipe in pipes: # Collision with pipe
        if bird.colliderect(pipe):
            return False
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return False
    for enemy in enemies: # Collision with enemy
        if bird.colliderect(enemy):
            return False
    return True