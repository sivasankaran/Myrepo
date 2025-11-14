import pygame
import random
import sys

# Simple Snake game using pygame
# Run with: python snake.py

# Game settings
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # each cell is 20x20 px
GRID_W = WIDTH // GRID_SIZE
GRID_H = HEIGHT // GRID_SIZE
FPS = 10  # speed; increase for a harder game

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 20, 60)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_empty_cell(exclude):
    """Return a random grid position not in the exclude set."""
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in exclude:
            return pos


def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))


def draw_rect_cell(surface, color, cell):
    x, y = cell
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def main():
    pygame.init()
    pygame.display.set_caption("Snake - Python/Pygame")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # Initial snake centered
    snake = [(GRID_W // 2 + i, GRID_H // 2) for i in range(2, -1, -1)]  # 3 segments
    direction = RIGHT

    # Place initial food not on snake
    snake_set = set(snake)
    food = random_empty_cell(snake_set)

    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                if not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                        direction = UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                        direction = DOWN
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                        direction = LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                        direction = RIGHT
                else:
                    if event.key in (pygame.K_SPACE, pygame.K_r):
                        # Reset game
                        snake = [(GRID_W // 2 + i, GRID_H // 2) for i in range(2, -1, -1)]
                        direction = RIGHT
                        snake_set = set(snake)
                        food = random_empty_cell(snake_set)
                        score = 0
                        game_over = False

        if not game_over:
            # Move snake
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = ((head_x + dx) % GRID_W, (head_y + dy) % GRID_H)  # wrap around

            # Check self-collision
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    snake_set = set(snake)
                    food = random_empty_cell(snake_set)
                else:
                    snake.pop()

        # Draw
        screen.fill(BLACK)
        draw_grid(screen)
        # draw food and snake
        draw_rect_cell(screen, RED, food)
        for i, seg in enumerate(snake):
            color = GREEN if i == 0 else (0, 160, 0)
            draw_rect_cell(screen, color, seg)

        # HUD
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 8))

        if game_over:
            msg1 = font.render("Game Over - Press R or Space to Restart, Q/Esc to Quit", True, WHITE)
            msg2 = font.render("Controls: Arrow Keys or WASD", True, WHITE)
            screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
