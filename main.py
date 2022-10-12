from engines.random_walk_engine import RandomWalkEngine
from engines.dfs_engine import DepthFirstSearchEngine
from engines.a_star_engine import AStarEngine
from engines.engine import SnakeEngine

import game_modes.single_game
import game_modes.adversary_game

# 0 = single AI
# 1 = dual AI
game_mode = 0

# moves {1:up, 2:right, 3:down, 4:left}

if game_mode == 0:
    game_modes.single_game.run_game(SnakeEngine)
elif game_mode == 1:
    game_modes.adversary_game.run_game(DepthFirstSearchEngine, SnakeEngine)
