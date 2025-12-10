import pygame
import random
from enum import Enum
from collections import deque

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self, start_x, start_y, color):
        self.body = deque([(start_x, start_y)])
        self.direction = Direction.RIGHT
        self.color = color
        self.grow_pending = False

    def move(self):
        dx, dy = self.direction.value
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)
        
        # Check self collision
        if new_head in self.body:
            return False
        
        self.body.appendleft(new_head)
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
        return True

    def grow(self):
        self.grow_pending = True

    def change_direction(self, new_direction):
        # Prevent reversing into itself
        dx_new, dy_new = new_direction.value
        dx_cur, dy_cur = self.direction.value
        if (dx_new, dy_new) != (-dx_cur, -dy_cur):
            self.direction = new_direction

    def draw(self, screen, block_size):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            # Head is brighter
            if i == 0:
                pygame.draw.rect(screen, tuple(min(c + 50, 255) for c in self.color), rect)
            else:
                pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

class SnakeGame:
    def __init__(self, width=800, height=600, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid_width = width // block_size
        self.grid_height = height // block_size
        
        # Initialize two snakes
        self.snake1 = Snake(5, 5, (255, 0, 0))  # Red snake
        self.snake2 = Snake(self.grid_width - 10, self.grid_height - 10, (255, 165, 0))  # Orange snake
        
        self.food = self._generate_food()
        self.score1 = 0
        self.score2 = 0
        self.game_over = False

    def _generate_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            food_pos = (x, y)
            
            # Ensure food doesn't spawn on either snake
            if food_pos not in self.snake1.body and food_pos not in self.snake2.body:
                return food_pos

    def update(self):
        if self.game_over:
            return
        
        # Move both snakes
        snake1_alive = self.snake1.move()
        snake2_alive = self.snake2.move()
        
        if not snake1_alive or not snake2_alive:
            self.game_over = True
            return
        
        # Check wall collisions for snake1
        if self._check_wall_collision(self.snake1):
            self.game_over = True
            return
        
        # Check wall collisions for snake2
        if self._check_wall_collision(self.snake2):
            self.game_over = True
            return
        
        # Check snake-to-snake collisions
        if self.snake1.body[0] in self.snake2.body or self.snake2.body[0] in self.snake1.body:
            self.game_over = True
            return
        
        # Check food collision for snake1
        if self.snake1.body[0] == self.food:
            self.snake1.grow()
            self.score1 += 10
            self.food = self._generate_food()
        
        # Check food collision for snake2
        if self.snake2.body[0] == self.food:
            self.snake2.grow()
            self.score2 += 10
            self.food = self._generate_food()

    def _check_wall_collision(self, snake):
        x, y = snake.body[0]
        return x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height

    def draw(self, screen):
        # Green background
        screen.fill((34, 139, 34))  # Forest green
        
        # Draw food (yellow)
        food_x, food_y = self.food
        pygame.draw.rect(screen, (255, 255, 0), 
                        (food_x * self.block_size, food_y * self.block_size, 
                         self.block_size, self.block_size))
        
        # Draw both snakes
        self.snake1.draw(screen, self.block_size)
        self.snake2.draw(screen, self.block_size)
        
        # Draw scores
        font = pygame.font.Font(None, 36)
        score1_text = font.render(f"Snake1 (Red): {self.score1}", True, (255, 0, 0))
        score2_text = font.render(f"Snake2 (Orange): {self.score2}", True, (255, 165, 0))
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (10, 50))
        
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (self.width // 2 - 200, self.height // 2 - 36))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Two-Player Snake Game")
    clock = pygame.time.Clock()
    
    game = SnakeGame()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Snake1 controls (Arrow keys)
                if event.key == pygame.K_UP:
                    game.snake1.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.snake1.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.snake1.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.snake1.change_direction(Direction.RIGHT)
                
                # Snake2 controls (WASD keys)
                elif event.key == pygame.K_w:
                    game.snake2.change_direction(Direction.UP)
                elif event.key == pygame.K_s:
                    game.snake2.change_direction(Direction.DOWN)
                elif event.key == pygame.K_a:
                    game.snake2.change_direction(Direction.LEFT)
                elif event.key == pygame.K_d:
                    game.snake2.change_direction(Direction.RIGHT)
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
