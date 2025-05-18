import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Levels")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Clock
clock = pygame.time.Clock()
base_speed = 10

# Snake and direction
snake = [(5, 5)]
direction = (1, 0)

# Obstacles (initialize before using in food function)
obstacles = []

# Font
font = pygame.font.SysFont("arial", 20)

# Food
def generate_food():
    while True:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if pos not in snake and pos not in obstacles:
            return pos

food = generate_food()

# Obstacles by level
def get_obstacles(level):
    obs = []
    if level >= 2:
        for i in range(10, 20):
            obs.append((i, 10))  # horizontal wall
    if level >= 3:
        for i in range(5, 15):
            obs.append((15, i))  # vertical wall
    return obs

# Get level
def get_level():
    return max(1, len(snake) // 5)

# Get speed based on level
def get_speed():
    return base_speed + get_level() - 1

# Draw everything
def draw_window():
    win.fill(BLACK)

    # Draw snake
    for x, y in snake:
        pygame.draw.rect(win, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw food
    fx, fy = food
    pygame.draw.rect(win, RED, (fx*CELL_SIZE, fy*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw obstacles
    for ox, oy in obstacles:
        pygame.draw.rect(win, GRAY, (ox*CELL_SIZE, oy*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw level
    level_text = font.render(f"Level: {get_level()}", True, WHITE)
    win.blit(level_text, (10, 10))

    pygame.display.update()

# Move snake
def move_snake():
    global food
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Collision with wall or self or obstacles
    if (new_head[0] < 0 or new_head[0] >= COLS or
        new_head[1] < 0 or new_head[1] >= ROWS or
        new_head in snake or
        new_head in obstacles):
        game_over()

    snake.insert(0, new_head)

    # Eat food or move
    if new_head == food:
        food = generate_food()
    else:
        snake.pop()

# Game over screen
def game_over():
    text = font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
    win.blit(text, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Restart game
def restart_game():
    global snake, direction, food
    snake = [(5, 5)]
    direction = (1, 0)
    food = generate_food()
    main()

# Main loop
def main():
    global direction, obstacles
    while True:
        clock.tick(get_speed())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, 1):
            direction = (0, -1)
        if keys[pygame.K_DOWN] and direction != (0, -1):
            direction = (0, 1)
        if keys[pygame.K_LEFT] and direction != (1, 0):
            direction = (-1, 0)
        if keys[pygame.K_RIGHT] and direction != (-1, 0):
            direction = (1, 0)

        obstacles = get_obstacles(get_level())
        move_snake()
        draw_window()

# Run the game
main()
