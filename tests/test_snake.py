import unittest
from unittest.mock import patch
import snake as s


class TestSnakeLivesAndLogic(unittest.TestCase):
    def test_life_decrement_and_reset_on_self_collision_with_lives_remaining(self):
        # Shape causes collision when moving DOWN: new head (2,3) equals existing body cell (2,3)
        snake = [(2, 2), (2, 3), (3, 3), (3, 2)]
        direction = s.DOWN
        food = (0, 0)  # far from the snake; not eaten
        score = 0
        lives = 2

        snake2, direction2, food2, score2, lives2, game_over = s.step_state(
            snake, direction, food, score, lives
        )

        self.assertEqual(lives2, 1)
        self.assertFalse(game_over)
        self.assertEqual(snake2, s.initial_snake())
        self.assertEqual(direction2, s.RIGHT)
        self.assertEqual(score2, 0)
        self.assertEqual(food2, food)  # unchanged since it doesn't overlap after reset

    def test_game_over_when_no_lives_left(self):
        snake = [(2, 2), (2, 3), (3, 3), (3, 2)]
        direction = s.DOWN
        food = (0, 0)
        score = 0
        lives = 1

        snake2, direction2, food2, score2, lives2, game_over = s.step_state(
            snake, direction, food, score, lives
        )

        self.assertEqual(lives2, 0)
        self.assertTrue(game_over)

    def test_normal_move_no_collision_no_eat(self):
        snake = s.initial_snake()
        direction = s.RIGHT
        food = (-1, -1)  # invalid grid cell but safe for equality checks (won't be eaten)
        score = 0
        lives = s.LIVES_DEFAULT

        snake2, direction2, food2, score2, lives2, game_over = s.step_state(
            snake, direction, food, score, lives
        )

        self.assertFalse(game_over)
        # Expected new head one step to the right; tail removed
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = ((head_x + dx) % s.GRID_W, (head_y + dy) % s.GRID_H)
        expected_snake = [new_head] + snake[:-1]

        self.assertEqual(snake2, expected_snake)
        self.assertEqual(lives2, lives)
        self.assertEqual(score2, score)
        self.assertEqual(direction2, direction)
        self.assertEqual(food2, food)

    @patch('snake.random_empty_cell', return_value=(1, 1))
    def test_eat_food_increases_score_and_grows(self, mock_rand_cell):
        snake = s.initial_snake()
        direction = s.RIGHT
        # Place food at the next head position so snake eats
        head_x, head_y = snake[0]
        dx, dy = direction
        food = ((head_x + dx) % s.GRID_W, (head_y + dy) % s.GRID_H)
        score = 0
        lives = s.LIVES_DEFAULT

        snake2, direction2, food2, score2, lives2, game_over = s.step_state(
            snake, direction, food, score, lives
        )

        self.assertFalse(game_over)
        self.assertEqual(score2, score + 1)
        self.assertEqual(len(snake2), len(snake) + 1)  # grew by 1
        self.assertEqual(food2, (1, 1))  # mocked placement
        self.assertEqual(lives2, lives)
        self.assertEqual(direction2, direction)


if __name__ == '__main__':
    unittest.main()
