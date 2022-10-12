#from engines.engine import SnakeEngine

class DepthFirstSearchEngine():
    def __init__(self, grid_size, head):
        self._grid_size = grid_size
        self._next_moves = []
        self._grid = []

    def get_engine_name(self):
        return 'Depth First Search'

    def get_next_move(self, grid, head):
        if len(self._next_moves) < 1:
            self._grid = grid
            self._graph = self._calculate_graph(grid)
            next_path = self._get_next_path_start(head)
            if next_path == None:
                return [1]
            self._next_moves = self._get_next_moves(next_path)
        return self._next_moves.pop()

    def _calculate_graph(self, grid):
        self._grid = grid
        graph = {}
        snake_values = [1, 2, 3, 4]
        for row_idx in range(len(grid)):
            for col_idx in range(len(grid[row_idx])):
                neighbors = []
                if row_idx != 0 and grid[row_idx - 1][col_idx] not in snake_values:
                    neighbors.append((row_idx - 1, col_idx))
                if row_idx != self._grid_size - 1 and grid[row_idx + 1][col_idx] not in snake_values:
                    neighbors.append((row_idx + 1, col_idx))
                if col_idx != self._grid_size - 1 and grid[row_idx][col_idx + 1] not in snake_values:
                    neighbors.append((row_idx, col_idx + 1))
                if col_idx != 0 and grid[row_idx][col_idx - 1] not in snake_values:
                    neighbors.append((row_idx, col_idx - 1))

                graph[(row_idx, col_idx)] = neighbors
        
        return graph

    def _get_next_path_start(self, head):
        if len(self._graph[(head['y'], head['x'])]) < 1:
            return 1 # If we're trapped, just return a direction, we're dead either way

        visited = [(head['y'], head['x'])]
        for neighbor in self._graph[(head['y'], head['x'])]:
            path = self._get_next_path(neighbor, visited)
            if path is not None:
                path.append((head['y'], head['x']))
                return path
        return [self._graph[(head['y'], head['x'])][0], (head['y'], head['x'])] # If we don't have access to the apple, just go to one of the neighbors and recalculate on the next move

    def _get_next_path(self, node, visited):
        visited.append(node)
        if self._grid[node[0]][node[1]] == 5:
            return [node]
        else:
            for neighbor in self._graph[node]:
                if neighbor not in visited:
                    path = self._get_next_path(neighbor, visited)
                    if path is not None:
                        path.append(node)
                        return path
            return None

    def _get_next_moves(self, next_path):
        next_moves = []
        current_node = next_path.pop()
        while len(next_path) > 0:
            next_node = next_path.pop()
            if current_node[0] == next_node[0]:
                if current_node[1] < next_node[1]:
                    next_moves.append(2)
                else:
                    next_moves.append(4)
            else:
                if current_node[0] < next_node[0]:
                    next_moves.append(3)
                else:
                    next_moves.append(1)
            current_node = next_node
        next_moves.reverse()
        return next_moves
