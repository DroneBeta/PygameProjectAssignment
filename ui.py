import pygame
import sys

def display_score(font, score, WHITE, screen):
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_button(text, x, y, width, height, screen, font, BLACK, WHITE, hover=False):
    #Draws a button and checks for hover effect
    color = WHITE if hover else (200, 200, 200)
    pygame.draw.rect(screen, color, (x, y, width, height))
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

def display_menu():
    #Display the main menu
    screen.fill(BLACK)
    title_text = font.render("Flappy Bird", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def display_game_over(WIDTH, HEIGHT, screen, BLACK, WHITE, font, score):
    #Display the game over screen with a button.
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    final_score_text = font.render(f"Score: {score}", True, WHITE)

    # Game over button: "Back to Menu"
    button_x, button_y = WIDTH // 2 - 100, HEIGHT // 2 + 100
    button_width, button_height = 200, 50
    draw_button("Back to Menu", button_x, button_y, button_width, button_height, screen, font, BLACK, WHITE, hover=False)

    # Display texts
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()