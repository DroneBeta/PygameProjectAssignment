import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Bird properties
bird = pygame.Rect(50, HEIGHT // 2, 30, 30)
BIRD_COLOR = BLUE
BIRD_GRAVITY = 0.5
BIRD_JUMP = -10

# Pipes properties
PIPE_WIDTH = 50
PIPE_COLOR = GREEN
PIPE_GAP = 150
PIPE_SPEED = 3
pipes = []

# Game properties
gravity = BIRD_GRAVITY
bird_movement = 0
score = 0
font = pygame.font.Font(None, 50)
game_active = True

def create_pipe():
    height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= PIPE_SPEED
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return False
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return False
    return True

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game loop
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = BIRD_JUMP
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird.center = (50, HEIGHT // 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird.y += bird_movement

        # Pipe movement
        pipes = move_pipes(pipes)
        
        # Check for collisions
        game_active = check_collision(pipes)

        # Score update
        for pipe in pipes:
            if pipe.centerx == bird.centerx:
                score += 0.5

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, BIRD_COLOR, bird)
    draw_pipes(pipes)
    display_score()

    pygame.display.flip()
    clock.tick(60)