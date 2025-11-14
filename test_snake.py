import unittest
import importlib
import types

# We import the snake module. Some pygame initialization inside main() won't run on import.
snake = importlib.import_module('snake')


class SnakeLogicTests(unittest.TestCase):
    def test_random_empty_cell_excludes_snake_positions(self):
        # Prepare a set of occupied cells
        occupied = {(1, 1), (2, 2), (3, 3)}
        # Call the helper multiple times to decrease flakiness
        for _ in range(20):
            pos = snake.random_empty_cell(occupied)
            self.assertNotIn(pos, occupied)
            # also ensure the position is within grid bounds
            x, y = pos
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, snake.GRID_W)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, snake.GRID_H)

    def test_grid_dimensions_match_window(self):
        # Ensure grid size factors match width/height
        self.assertEqual(snake.WIDTH // snake.GRID_SIZE, snake.GRID_W)
        self.assertEqual(snake.HEIGHT // snake.GRID_SIZE, snake.GRID_H)
        # No partial cells should remain
        self.assertEqual(snake.WIDTH % snake.GRID_SIZE, 0)
        self.assertEqual(snake.HEIGHT % snake.GRID_SIZE, 0)

    def test_direction_constants(self):
        # Basic sanity checks on direction constants
        self.assertEqual(snake.UP, (0, -1))
        self.assertEqual(snake.DOWN, (0, 1))
        self.assertEqual(snake.LEFT, (-1, 0))
        self.assertEqual(snake.RIGHT, (1, 0))

    def test_wrap_movement_math(self):
        # Simulate a head at edges and apply wrap logic like in main()
        def move(head, direction):
            x, y = head
            dx, dy = direction
            return ((x + dx) % snake.GRID_W, (y + dy) % snake.GRID_H)

        # Right edge wraps to 0
        head = (snake.GRID_W - 1, 5)
        self.assertEqual(move(head, snake.RIGHT), (0, 5))
        # Left edge wraps to GRID_W - 1
        head = (0, 5)
        self.assertEqual(move(head, snake.LEFT), (snake.GRID_W - 1, 5))
        # Bottom edge wraps to 0
        head = (3, snake.GRID_H - 1)
        self.assertEqual(move(head, snake.DOWN), (3, 0))
        # Top edge wraps to GRID_H - 1
        head = (3, 0)
        self.assertEqual(move(head, snake.UP), (3, snake.GRID_H - 1))

    def test_self_collision_detection(self):
        # Use a simple snake body and try to move the head into the body
        snake_body = [(5, 5), (5, 6), (5, 7)]
        direction = snake.DOWN  # moving into (5,6)
        head_x, head_y = snake_body[0]
        dx, dy = direction
        new_head = ((head_x + dx) % snake.GRID_W, (head_y + dy) % snake.GRID_H)
        self.assertIn(new_head, snake_body)

    def test_food_not_on_snake(self):
        # Create a full row snake; ensure food not spawned on any part of it
        snake_body = [(x, 0) for x in range(min(10, snake.GRID_W))]
        for _ in range(20):
            food = snake.random_empty_cell(set(snake_body))
            self.assertNotIn(food, snake_body)


if __name__ == '__main__':
    unittest.main()
