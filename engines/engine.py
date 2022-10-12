import random
from engines.dfs_engine import DepthFirstSearchEngine
#5815

class SnakeEngine(DepthFirstSearchEngine):

    def __init__(self, grid_size, head):
        self._grid_size = grid_size
        self._head = head
        self.length = 4
        self.start = 1
        self.direction = 1 #1 = up, 3 = down
        self.possible_moves = [1, 2, 3, 4]
        self.dfs_engine = DepthFirstSearchEngine(grid_size)

    def get_engine_name(self):
        return 'Default Engine'

    def set_snake_length(self, grid):
        self.length = 0
        for row in grid:
            for cell in row:
                if cell in [1, 2, 3, 4]: self.length += 1

    def get_next_move(self, grid, head, tail, direction, apple):
        self.set_snake_length(grid)
        self.calc_possible_moves(grid, head)
        self.dfs_engine(grid, head)

        if self.length < self._grid_size*2-1:
            return self.start_method(grid, head, apple)
        
        elif self.length < 50:
            return self.dfs_engine(grid, head)

    def start_method(self, grid, head, apple):
        #if at the top, go right or left until the head is above the apple
        move = 1
        if head['y'] == 0: 
            if head['x'] > apple['x']: 
                move = 4
            elif head['x'] < apple['x']:
                move = 2
            else:
                self.direction = 3 #set direction "mode" to downward
                move = 3

        #head down to bottom, collecting apple on the way
        elif self.direction == 3 and (head['x'] == apple['x'] or head['y'] != self._grid_size-1):
            move = 3

        #if at the bottom, go right or left until the head is above the apple
        elif head['y'] == self._grid_size-1:
            self.direction = 1 #once the snake hits the bottom, set direction "mode" to upwards
            if head['x'] > apple['x']:
                move = 4
            elif head['x'] < apple['x']:
                move = 2
            else:
                move = 1

        #head to top, collecting apple on the way
        elif self.direction == 1 and (head['x'] == apple['x'] or head['y'] != 0):
            move = 1
    
        if move not in self.possible_moves:
            result = self.dfs_engine(grid, head)
            print(result)
            return result

        return move

    def calc_possible_moves(self, grid, head):
        snake_values = [1, 2, 3, 4]
        self.possible_moves = []
        if head['y'] != 0 and grid[head['y'] - 1][head['x']] not in snake_values:
            self.possible_moves.append(1)
        if head['y'] != self._grid_size - 1 and grid[head['y'] + 1][head['x']] not in snake_values:
            self.possible_moves.append(3)
        if head['x'] != self._grid_size - 1 and grid[head['y']][head['x'] + 1] not in snake_values:
            self.possible_moves.append(2)
        if head['x'] != 0 and grid[head['y']][head['x'] - 1] not in snake_values:
            self.possible_moves.append(4)