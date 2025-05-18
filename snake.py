import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window and Grid settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI Game - User Places Food")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Game Clock and Speed
clock = pygame.time.Clock()
base_speed = 10

# Font
font = pygame.font.SysFont("arial", 20)

# Snake and direction
snake = [(5, 5)]
direction = (1, 0)

# Obstacles
obstacles = []

# Food - initially none (user will place)
food = None

# Obstacles based on level
def get_obstacles(level):
    obs = []
    if level >= 2:
        for i in range(10, 20):
            obs.append((i, 10))
    if level >= 3:
        for i in range(5, 15):
            obs.append((15, i))
    return obs

# Get level
def get_level():
    return max(1, len(snake) // 5)

# Get speed
def get_speed():
    return base_speed + get_level() - 1

# Draw everything
def draw_window():
    win.fill(BLACK)

    for x, y in snake:
        pygame.draw.rect(win, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if food:
        fx, fy = food
        pygame.draw.rect(win, RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for ox, oy in obstacles:
        pygame.draw.rect(win, GRAY, (ox * CELL_SIZE, oy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    level_text = font.render(f"Level: {get_level()}", True, WHITE)
    win.blit(level_text, (10, 10))

    instruction_text = font.render("Click to place food", True, WHITE)
    win.blit(instruction_text, (WIDTH - 180, 10))

    pygame.display.update()

# Move snake
def move_snake():
    global food
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Check collisions
    if (new_head[0] < 0 or new_head[0] >= COLS or
        new_head[1] < 0 or new_head[1] >= ROWS or
        new_head in snake or
        new_head in obstacles):
        game_over()

    snake.insert(0, new_head)

    if food and new_head == food:
        # Snake ate the food, remove food from board (wait for next user placement)
        food = None
    else:
        snake.pop()

# Game over
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

# Restart
def restart_game():
    global snake, direction, food
    snake.clear()
    snake.append((5, 5))
    direction = (1, 0)
    food = None
    main()

# AI logic: move toward food
def get_ai_direction(snake, food, obstacles):
    if not food:
        return direction  # Keep going same way if no food

    head = snake[0]
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
    safe_moves = []

    for d in directions:
        new_head = (head[0] + d[0], head[1] + d[1])
        if (0 <= new_head[0] < COLS and
            0 <= new_head[1] < ROWS and
            new_head not in snake and
            new_head not in obstacles):
            safe_moves.append((d, new_head))

    if safe_moves:
        # Sort moves by Manhattan distance to food
        safe_moves.sort(key=lambda move: abs(move[1][0] - food[0]) + abs(move[1][1] - food[1]))
        return safe_moves[0][0]

    return (0, 0)  # No safe move

# Main loop
def main():
    global direction, obstacles, food
    while True:
        clock.tick(get_speed())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # User places food on click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                grid_x = mx // CELL_SIZE
                grid_y = my // CELL_SIZE
                if (grid_x, grid_y) not in snake and (grid_x, grid_y) not in obstacles:
                    food = (grid_x, grid_y)

            # Restart/Quit handled in game_over only

        obstacles = get_obstacles(get_level())
        direction = get_ai_direction(snake, food, obstacles)
        move_snake()
        draw_window()

# Start game
main()
