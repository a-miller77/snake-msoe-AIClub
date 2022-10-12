import random
from engines.engine import SnakeEngine

class RandomWalkEngine(SnakeEngine):
    def __init__(self, grid_size, head):
        super().__init__(grid_size, head)

    def get_engine_name(self):
        return 'Random Walk'

    def get_next_move(self, grid, head, tail, direction, apple):
        snake_values = [1, 2, 3, 4]
        possible_directions = []
        if head['y'] != 0 and grid[head['y'] - 1][head['x']] not in snake_values:
            possible_directions.append(1)
        if head['y'] != self._grid_size - 1 and grid[head['y'] + 1][head['x']] not in snake_values:
            possible_directions.append(3)
        if head['x'] != self._grid_size - 1 and grid[head['y']][head['x'] + 1] not in snake_values:
            possible_directions.append(2)
        if head['x'] != 0 and grid[head['y']][head['x'] - 1] not in snake_values:
            possible_directions.append(4)

        num_possible_moves = len(possible_directions)
        if num_possible_moves < 1:
            return 1
        move_idx = random.randint(0, num_possible_moves-1)
        return possible_directions[move_idx]
