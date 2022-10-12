import random
import pygame
import math

def run_game(ai_engine):
    pygame.init()
    clock = pygame.time.Clock()

    tick_count = 0
    ticks_per_second = 20
    move_speed = 100

    colors = {
        'snake':(0, 200, 0)
        ,'background':(0, 0, 0)
        ,'apple':(255, 0, 0)
    }

    grid_size = 18  # Number of horizontal and vertical tiles
    tile_size = 35  # Pixel size of each tile
    line_size = 4  # Number of pixels between each tile
    window_size = tile_size * grid_size + line_size * (grid_size + 1)

    screen = pygame.display.set_mode((window_size, window_size))

    # The value inside direction is the direction of the snake head
    # 1 = up, 2 = right, 3 = down, 4 = left
    direction = [2]

    snake_length = 4

    # Start positions
    head = {"x": 4, "y": math.floor((grid_size/2))}
    tail = {"x": head["x"]-snake_length+1, "y": math.floor((grid_size/2))}
    apple = {"x": grid_size-1, "y": math.floor((grid_size/2))}

    ai_game = True
    ai_engine = ai_engine(grid_size, head)

    previous_tail = {"x": 0, "y": 0} # Used to delete the previous tail position after moving the snake


    def draw_tile(x, y, color):
        pygame.draw.rect(screen, color,
                        ((tile_size + line_size) * x,(tile_size + line_size) * y,
                        tile_size + line_size *2, tile_size + line_size *2))


    def draw_apple(x, y):
        pygame.draw.rect(screen, colors['apple'],
            (line_size + (tile_size + line_size) * x, line_size + (tile_size + line_size) * y,
            tile_size, tile_size)
        )

    def draw_snake(x, y, direction):
        if direction == 1: # up
            pygame.draw.rect(screen, colors['snake'],
                (line_size + (tile_size + line_size) * x, 
                line_size + (tile_size + line_size) * y,
                tile_size, 
                tile_size + line_size)
            ) 
        elif direction == 3: # down
            pygame.draw.rect(screen, colors['snake'],
                (line_size + (tile_size + line_size) * x, 
                (tile_size + line_size) * y,
                tile_size, 
                tile_size + line_size)
            ) 
        elif direction == 2: # right
            pygame.draw.rect(screen, colors['snake'],
                ((tile_size + line_size) * x, 
                line_size + (tile_size + line_size) * y,
                tile_size + line_size,
                tile_size)
            ) 
        elif direction == 4: # left
            pygame.draw.rect(screen, colors['snake'],
                (line_size + (tile_size + line_size) * x, 
                line_size + (tile_size + line_size) * y,
                tile_size + line_size,
                tile_size)
            ) 
        else:
            pygame.draw.rect(screen, colors['snake'],
                (line_size + (tile_size + line_size) * x, 
                line_size + (tile_size + line_size) * y,
                tile_size, 
                tile_size)
            )

    # Create 2-dimensional grid representing the game, and draw it on the screen
    grid = []
    for y in range(grid_size):
        grid.append([])
        for x in range(grid_size):
            grid[y].append(0)
            draw_tile(x, y, colors['background'])

    # Place and draw snake
    for i in range(snake_length):
        y = math.floor((grid_size/2))
        grid[y][tail["x"]+i] = 2
        draw_snake(tail["x"]+i, y, 2)#colors['snake'])

    # Place and draw apple
    grid[apple["y"]][apple["x"]] = 5
    draw_apple(apple["x"], apple["y"])
                
    def move_snake_part(snake_part):
        # The snake part will read the value inside it's own position and move based on it.

        if grid[snake_part["y"]][snake_part["x"]] == 1:
            snake_part["y"] -= 1
        elif grid[snake_part["y"]][snake_part["x"]] == 2:
            snake_part["x"] += 1
        elif grid[snake_part["y"]][snake_part["x"]] == 3:
            snake_part["y"] += 1
        elif grid[snake_part["y"]][snake_part["x"]] == 4:
            snake_part["x"] -= 1

    #base_save_directory = 'game_saves/game_'
    save_index = 0
    # save_directory = base_save_directory + str(save_index)
    # while os.path.exists(save_directory):
    #     save_index += 1
    #     save_directory = base_save_directory + str(save_index)
    # os.mkdir(save_directory)
    # save_directory += '/'
    # print('Game saving to directory:' + save_directory)
    game_data = {
        'ai_engine': ai_engine.get_engine_name(),
        'ai_game'  : ai_game,
        'grid_size': grid_size
    }
    # with open(save_directory + 'game_details.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(game_data))

    turn_number = 0

    # Game loop
    while True:

        tick_count += 1
        if tick_count > ticks_per_second/move_speed:
            turn_number += 1
            print('turn_number: ' + str(turn_number), end='\r')

            if not ai_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            direction.append(1)
                        elif event.key == pygame.K_RIGHT:
                            direction.append(2)
                        elif event.key == pygame.K_DOWN:
                            direction.append(3)
                        elif event.key == pygame.K_LEFT:
                            direction.append(4)
            else:
                direction.append(ai_engine.get_next_move(grid, head, tail, direction, apple))

            tick_count = 0

            # The main idea is that the head will lay a path which the tail can follow.
            # The tail will delete the path while it moves through it, 
            # which means that the path between the head and the tail equals the whole snake.
            # Collisions can then be added by checking if the head moves into the path it has laid down.

            # Change direction if keypresses have been queued
            if len(direction) > 1:
                direction.pop(0)
                grid[head["y"]][head["x"]] = direction[0]

            move_snake_part(head)
            # Check collision with walls
            if head["x"] < 0 or head["x"] > grid_size-1 or head["y"] < 0 or head["y"] > grid_size-1:
                quit()

            # Only move the tail if an apple has not been eaten
            # Not moving the tail will result in the snake getting longer
            if grid[head["y"]][head["x"]] != 5:

                # Remember previous tail position so that the used path can be deleted
                previous_tail["x"] = tail["x"]
                previous_tail["y"] = tail["y"]

                # The tail will follow path laid by head
                move_snake_part(tail)

                # Delete used path
                grid[previous_tail["y"]][previous_tail["x"]] = 0
                draw_tile(previous_tail["x"], previous_tail["y"], colors['background'])

            else:
                # Add new apple in random position. The new position must be empty
                while grid[apple["y"]][apple["x"]] != 0:
                    apple["x"] = random.randint(0, grid_size - 1)
                    apple["y"] = random.randint(0, grid_size - 1)
                grid[apple["y"]][apple["x"]] = 5
                draw_apple(apple["x"], apple["y"])

            # Check collision with itself. 5 = apple, 0 = empty, all other values = snake
            if grid[head["y"]][head["x"]] != 5 and grid[head["y"]][head["x"]] != 0:
               quit()

            # lay down path for tail
            grid[head["y"]][head["x"]] = direction[0]
            # draw_tile(head["x"], head["y"], colors['snake'])
            draw_snake(head["x"], head["y"], direction[0])
        

            pygame.display.update()

        clock.tick(ticks_per_second)