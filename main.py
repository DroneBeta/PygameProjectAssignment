import pygame
import sys
import random

from bullet import *
from drawCalls import *
from ui import *

# Initialize pygame
pygame.init()


def difficulty_up(PIPE_GAP, score, spawn_rate, SPAWNPIPE):
    # Update PIPE_GAP
    if score % 5 == 0:
        PIPE_GAP = max(60, 220 - score // 10)
    # Update spawn rate
    if score % 5 == 0:  # Decrease spawn rate every 50 points
        new_spawn_rate = max(1000, 2000 - score * 2)
        if new_spawn_rate != spawn_rate:  # Only update if spawn rate has changed
            pygame.time.set_timer(SPAWNPIPE, int(new_spawn_rate))
            spawn_rate = new_spawn_rate
    return PIPE_GAP, spawn_rate


def main_loop():

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 255)

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Bat Killer")

    # Animations
    bat_animation = [
        pygame.image.load("Assets/player_up_flap.png").convert_alpha(),
        pygame.image.load("Assets/player_middle_flap.png").convert_alpha(),
        pygame.image.load("Assets/player_down_flap.png").convert_alpha(),
        pygame.image.load("Assets/player_shoot.png").convert_alpha()
    ]
    bat_index = 0
    bat_animation_resized = [pygame.transform.scale(frame, (60, 60)) for frame in bat_animation]

    enemy_animation = [
        pygame.image.load("Assets/evil_down_flap.png").convert_alpha(),
        pygame.image.load("Assets/evil_middle_flap.png").convert_alpha(),
        pygame.image.load("Assets/evil_up_flap.png").convert_alpha()
    ]
    enemy_index = 0
    enemy_animation_resized = [pygame.transform.scale(frame, (60, 60)) for frame in enemy_animation]

    background_images = [
        pygame.image.load("Assets/sky_box.png").convert_alpha(),
        pygame.image.load("Assets/mountain.png").convert_alpha(),
        pygame.image.load("Assets/floor.png").convert_alpha(),
        pygame.image.load("Assets/sun.png").convert_alpha(),
        pygame.image.load("Assets/cloud.png").convert_alpha()
    ]
    paralax_speed = [
        0,
        1,
        2,
        0.02,
        0.5
    ]

    paralax_position = [
        0,
        0,
        0,
        0,
        0
    ]


    # Properties of animation
    frame = 0
    bat_frame = 0
    frame_speed = 10

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Bird properties
    bird = pygame.Rect(50, HEIGHT // 2, 40, 40)
    BIRD_GRAVITY = 0.4
    BIRD_JUMP = -8

    # Pipes properties
    PIPE_WIDTH = 50
    PIPE_COLOR = (243,222,175)
    PIPE_GAP = 220
    PIPE_SPEED = 4
    pipes = []

    # Game properties
    gravity = BIRD_GRAVITY
    bird_movement = 0
    score = 0
    font = pygame.font.Font(None, 50)
    game_active = True
    game_state = "Game"
    spawn_rate = 2000
    spawn_update = False

    # Bullet properties
    bullets = []
    BULLET_RADIUS = 7
    BULLET_COLOR = (114,35,113)
    BULLET_SPEED = 20

    # Enemy properties
    ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40
    ENEMY_SPEED = PIPE_SPEED  # Move at the same speed as the pipes
    enemies = []
    enemy_amplitude = 1

    # Game loop
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, spawn_rate) # Rate of pipe spawned

    while True:
        if game_state != "Game":
            game_active = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state =="Menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "Game"
                        game_active = True
                        bird.center = (50, HEIGHT // 2)
                        bird_movement = 0
                        pipes.clear()
                        score = 0
                        continue
            elif game_state == "GameOver" :
                display_game_over(WIDTH, HEIGHT, screen, BLACK, WHITE, font, score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "Game"
                        game_active = True
                    continue
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and game_active: # Jump with 'Space Bar'
                    bird_movement = BIRD_JUMP
                    bat_index = 2
                    bat_frame = 0

                if event.key == pygame.K_SPACE and not game_active:
                    game_active = False
                    pipes.clear()
                    enemies.clear()
                    bird.center = (50, HEIGHT // 2)
                    bird_movement = 0
                    score = 0
                    game_state = "GameOver"
                if event.key == pygame.K_w and game_active:  # Shoot with 'W'
                    bullet_position = (bird.x + bird.width, bird.y + bird.height // 2 + 20)
                    bullets.append(bullet_position)
                    bat_index = 3


            if event.type == SPAWNPIPE:
                top_pipe, bottom_pipe = create_pipe(HEIGHT, WIDTH, PIPE_GAP, PIPE_WIDTH)
                pipes.append(bottom_pipe)
                pipes.append(top_pipe)

                # Difficulty ranking up
                if game_active:
                    PIPE_GAP, spawn_rate  = difficulty_up(PIPE_GAP, score, spawn_rate, SPAWNPIPE)

                if random.random() < 0.4: # Spawn an enemy with a 40% chance
                    enemy = spawn_enemy(pipes[len(pipes) - 1], PIPE_WIDTH, ENEMY_WIDTH, ENEMY_HEIGHT, PIPE_GAP) 
                    enemies.append(enemy)

        if game_active:
            # Bird movement
            bird_movement += gravity
            bird.y += bird_movement

            # Pipe movement
            pipes = move_pipes(pipes, PIPE_SPEED)

            # Bullets movement
            bullets = move_bullets(bullets, BULLET_SPEED, WIDTH)

            # Move enemies
            enemies = move_enemies(enemies, ENEMY_SPEED, enemy_amplitude)
        
            # Check for collisions
            game_active = check_collision(pipes, enemies, bird, HEIGHT)
            check_bullet_collisions(bullets, pipes, BULLET_RADIUS)

            # Score update
            for pipe in pipes:
                if bird.x == pipe.right:  
                    score += 2.5

            # Animation
            frame += 1
            bat_frame += 1
            if frame >= frame_speed:
                frame = 0
                enemy_index = (enemy_index + 1) % len(enemy_animation)

            if bat_frame >= frame_speed and bat_index != 0 and bat_index != 3:
                bat_index = (bat_index + 1) % 2
        
            # Drawing
            screen.fill(BLACK)
            background_animation(screen, background_images, paralax_position,  paralax_speed, game_active)
        
            current_frame = bat_animation_resized[bat_index]
            screen.blit(current_frame, bird.topleft)

            draw_pipes(pipes, PIPE_COLOR, screen)
            display_score(font, score, WHITE, screen) 
            draw_bullets(bullets, BULLET_COLOR, BULLET_RADIUS, screen)
            draw_enemies(enemies, enemy_index, enemy_animation_resized, screen)
            check_bullet_enemy_collisions(bullets, enemies, BULLET_RADIUS, score)


        pygame.display.flip()
        clock.tick(60)

main_loop ()