from engines.engine import SnakeEngine

class AStarEngine(SnakeEngine):
    def __init__(self, grid_size, head):
        self._grid_size = grid_size
        self._snake_values = [1, 2, 3, 4]
        self._next_moves = []
        self._grid = []
        self._head = ()
        self._apple = ()
        self._open = {}
        self._closed = {}

    def get_engine_name(self):
        return 'A*'

    def get_next_move(self, grid, head, tail, direction, apple):
        self._grid = grid
        self._head = head
        neighbors = self._get_neighbors(self._head)
        
        self._apple = apple
        self._open = {}
        self._open[(self._head['y'], self._head['x'])] = {'g': 0, 'h': 0, 'f':0, 'parent': None}
        self._closed = {}
        next_path = self._calculate_path(self._head)
        if next_path == None:
            if len(neighbors) < 1:
                return 1
            else:
                next_path = [neighbors[0], self._head]
        self._next_moves = self._get_next_moves(next_path)
        next_move = self._next_moves.pop()
        return next_move

    def _calculate_path(self, current_node):
        '''
            f is the 'value' of a node, the lower the value the better
            f = g + h 
            g is the distance from the starting node to the current node. 
                We can find this by adding the g of the previous node to the current node.
                In this example with Manhattan distances, g will always increase by 1
            h is the distance from the current node to the apple.
                We also find this via the Manhattan distance
        '''
        row_idx = current_node['y']
        col_idx = current_node['x']
        neighbors = []

        if row_idx == self._apple['y'] and col_idx == self._apple['x']:
            return [self._apple, self._open[(current_node['y'], current_node['x'])]['parent']]

        neighbors = self._get_neighbors(current_node)

        for node in neighbors:
            # If a node has not already been evaluated and put into the closed list
            # AND if a node hasn't already been calculated or we are approaching it from a more optimal path
            # Note that evaluating and calculating a node are different. Evaluating means we calculate all of it's neighbors' values
            g = self._open[(current_node['y'], current_node['x'])]['g'] + 1
            if (node['y'], node['x']) not in self._closed.keys() and ((node['y'], node['x']) not in self._open.keys() or self._open[(node['y'], node['x'])]['g'] > g):
                h = self._get_distance_between_nodes(self._apple, node)
                self._open[(node['y'], node['x'])] = {'g': g, 'h': h, 'f':g+h, 'parent': current_node} 

        self._closed[(current_node['y'], current_node['x'])] = self._open[(current_node['y'], current_node['x'])]
        del self._open[(current_node['y'], current_node['x'])]

        if not self._open:
            return None

        smallest_f = min([x['f'] for x in self._open.values()])
        nodes_with_smallest_fs = {}
        for k, v in self._open.items():
            if v['f'] == smallest_f:
                nodes_with_smallest_fs[k] = v
        
        smallest_h = min([x['h'] for x in nodes_with_smallest_fs.values()])
        for k, v in nodes_with_smallest_fs.items():
            if v['h'] == smallest_h:
                next_node = {'y':k[0], 'x':k[1]}
                break

        path = self._calculate_path(next_node)
        if path and current_node == path[-1] and current_node != self._head:
            path.append(self._closed[(current_node['y'], current_node['x'])]['parent'])
        return path

    def _get_distance_between_nodes(self, node1, node2):
        # Because the snake cannot travel diagonally, we calculate the Manhattan distance
        # A Manhattan distance means we do not allow diagonals (Euclidian distance)
        # A good vizualization can be seen here https://www.quora.com/What-is-Manhattan-Distance
        distance = 0
        distance += abs(node1['y'] - node2['y'])
        distance += abs(node1['x'] - node2['x'])
        return distance

    def _get_next_moves(self, next_path):
        next_moves = []
        current_node = next_path.pop()
        while len(next_path) > 0:
            next_node = next_path.pop()
            if current_node['y'] == next_node['y']:
                if current_node['x'] < next_node['x']:
                    next_moves.append(2)
                else:
                    next_moves.append(4)
            else:
                if current_node['y'] < next_node['y']:
                    next_moves.append(3)
                else:
                    next_moves.append(1)
            current_node = next_node
        next_moves.reverse()
        return next_moves

    def _get_neighbors(self, node):
        row_idx = node['y']
        col_idx = node['x']
        neighbors = []
        if row_idx != 0 and self._grid[row_idx - 1][col_idx] not in self._snake_values:
            neighbors.append({'y':row_idx - 1, 'x':col_idx})
        if row_idx != self._grid_size - 1 and self._grid[row_idx + 1][col_idx] not in self._snake_values:
            neighbors.append({'y':row_idx + 1, 'x':col_idx})
        if col_idx != self._grid_size - 1 and self._grid[row_idx][col_idx + 1] not in self._snake_values:
            neighbors.append({'y':row_idx, 'x':col_idx + 1})
        if col_idx != 0 and self._grid[row_idx][col_idx - 1] not in self._snake_values:
            neighbors.append({'y':row_idx, 'x':col_idx - 1})
        return neighbors
