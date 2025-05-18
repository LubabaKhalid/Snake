import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window and Grid settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI Game - Stage Select")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
snake_head_img = pygame.image.load('snake_head.jpg').convert_alpha()
snake_body_img = pygame.image.load('snake_image.jpg').convert_alpha()
food_img = pygame.image.load('food.png').convert_alpha()
obstacle_img = pygame.image.load('obstacle.png').convert_alpha()
background_img = pygame.image.load('background.png').convert()

# Load sounds
eat_sound = pygame.mixer.Sound('eat.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')

# Font
font = pygame.font.SysFont("arial", 20)

# Game Clock
clock = pygame.time.Clock()
base_speed = 10

# Globals that will be set in main()
snake = []
direction = (1, 0)
food = None
obstacles = []
stage = 1

# Obstacles based on level (stage)
def get_obstacles(level):
    obs = []
    if level >= 2:
        for i in range(10, 20):
            obs.append((i, 10))
    if level >= 3:
        for i in range(5, 15):
            obs.append((15, i))
    return obs

def get_level():
    # Fix level based on stage but allow grow beyond stage by length
    return max(stage, len(snake) // 5)

def get_speed():
    return base_speed + get_level() - 1

def draw_window():
    win.blit(background_img, (0, 0))

    for i, (x, y) in enumerate(snake):
        if i == 0:
            win.blit(snake_head_img, (x * CELL_SIZE, y * CELL_SIZE))
        else:
            win.blit(snake_body_img, (x * CELL_SIZE, y * CELL_SIZE))

    if food:
        fx, fy = food
        win.blit(food_img, (fx * CELL_SIZE, fy * CELL_SIZE))

    for ox, oy in obstacles:
        win.blit(obstacle_img, (ox * CELL_SIZE, oy * CELL_SIZE))

    level_text = font.render(f"Level: {get_level()}", True, WHITE)
    win.blit(level_text, (10, 10))

    score_text = font.render(f"Score: {len(snake) - 1}", True, WHITE)
    win.blit(score_text, (10, 40))

    instruction_text = font.render("Click to place food", True, WHITE)
    win.blit(instruction_text, (WIDTH - 180, 10))

    pygame.display.update()

def move_snake():
    global food
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Collisions
    if (new_head[0] < 0 or new_head[0] >= COLS or
        new_head[1] < 0 or new_head[1] >= ROWS or
        new_head in snake or
        new_head in obstacles):
        game_over()

    snake.insert(0, new_head)

    if food and new_head == food:
        eat_sound.play()
        food = None
    else:
        snake.pop()

def game_over():
    gameover_sound.play()
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

def restart_game():
    global snake, direction, food
    snake.clear()
    snake.append((5, 5))
    direction = (1, 0)
    food = None
    main()

def get_ai_direction(snake, food, obstacles):
    if not food:
        return direction

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
        safe_moves.sort(key=lambda move: abs(move[1][0] - food[0]) + abs(move[1][1] - food[1]))
        return safe_moves[0][0]

    return (0, 0)

def main():
    global direction, obstacles, food, stage, snake

    # Initialize snake and direction
    snake = [(5, 5)]
    direction = (1, 0)
    food = None
    obstacles = get_obstacles(stage)

    while True:
        clock.tick(get_speed())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                grid_x = mx // CELL_SIZE
                grid_y = my // CELL_SIZE
                if (grid_x, grid_y) not in snake and (grid_x, grid_y) not in obstacles:
                    food = (grid_x, grid_y)

            # Restart/Quit handled in game_over()

        # Update obstacles in case level changes
        obstacles = get_obstacles(get_level())

        direction = get_ai_direction(snake, food, obstacles)
        move_snake()
        draw_window()

# Run the game if this file is run directly:
if __name__ == "__main__":
    # Stage will be set by web page (Part 2)
    import sys
    if len(sys.argv) > 1:
        try:
            stage = int(sys.argv[1])
            if stage < 1:
                stage = 1
        except:
            stage = 1
    else:
        stage = 1

    main()
