import random
import pygame
import math

def run_game(ai_engine1, ai_engine2):
    tick_count = 0
    ticks_per_second = 10
    move_speed = 100
    snake_start_length = 4

    colors = {
        'background':(0, 0, 0)
        ,'apple':(255, 0, 0)
    }

    grid_size = 14  # Number of horizontal and vertical tiles
    tile_size = 35  # Pixel size of each tile
    line_size = 4  # Number of pixels between each tile
    x_padding_size = 10 # Number of pixels between games
    y_padding_size = 100
    window_size = tile_size * grid_size + line_size * (grid_size + 1)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((window_size+x_padding_size+window_size, window_size+y_padding_size))

    pygame.draw.rect(screen, (255, 255, 255),
                        (window_size, 0,
                        x_padding_size, window_size+y_padding_size))

    def draw_tile(x, y, color, offsetx, offsety):
        pygame.draw.rect(screen, color,
                        ((tile_size + line_size) * x + offsetx,(tile_size + line_size) * y + offsety,
                        tile_size + line_size * 2, tile_size + line_size * 2))

    def draw_apple(x, y, offsetx, offsety):
        pygame.draw.rect(screen, colors['apple'],
            (line_size + (tile_size + line_size) * x + offsetx, line_size + (tile_size + line_size) * y + offsety,
            tile_size, tile_size)
        )

    def draw_snake(x, y, direction, offsetx, offsety, color):
        if direction == 1: # up
            pygame.draw.rect(screen, color,
                (line_size + (tile_size + line_size) * x + offsetx, 
                line_size + (tile_size + line_size) * y + offsety,
                tile_size, 
                tile_size + line_size)
            ) 
        elif direction == 3: # down
            pygame.draw.rect(screen, color,
                (line_size + (tile_size + line_size) * x + offsetx, 
                (tile_size + line_size) * y + offsety,
                tile_size, 
                tile_size + line_size)
            ) 
        elif direction == 2: # right
            pygame.draw.rect(screen, color,
                ((tile_size + line_size) * x + offsetx, 
                line_size + (tile_size + line_size) * y + offsety,
                tile_size + line_size,
                tile_size)
            ) 
        else: # left
            pygame.draw.rect(screen, color,
                (line_size + (tile_size + line_size) * x + offsetx, 
                line_size + (tile_size + line_size) * y + offsety,
                tile_size + line_size,
                tile_size)
            ) 


    def make_grid(offsetx, offsety):
        # Create 2-dimensional grid representing the game, and draw it on the screen
        grid = []
        for y in range(grid_size):
            grid.append([])
            for x in range(grid_size):
                grid[y].append(0)
                draw_tile(x, y, colors['background'], offsetx, offsety)
        return grid

    def draw_snake_start(grid, tail, offsetx, offsety, color):
        # Place and draw snake
        for i in range(snake_start_length):
            y = math.floor((grid_size/2))
            grid[y][tail["x"]+i] = 2
            draw_snake(tail["x"]+i, y, 2, offsetx, offsety, color)

    def draw_apple_start(grid, apple, offsetx, offsety):
        # Place and draw apple
        grid[apple["y"]][apple["x"]] = 5
        draw_apple(apple["x"], apple["y"], offsetx, offsety)
                
    def move_snake_part(grid, snake_part):
        # The snake part will read the value inside it's own position and move based on it.
        if grid[snake_part["y"]][snake_part["x"]] == 1:
            snake_part["y"] -= 1
        elif grid[snake_part["y"]][snake_part["x"]] == 2:
            snake_part["x"] += 1
        elif grid[snake_part["y"]][snake_part["x"]] == 3:
            snake_part["y"] += 1
        elif grid[snake_part["y"]][snake_part["x"]] == 4:
            snake_part["x"] -= 1

    def move_snake_tail(grid, head, previous_tail, tail, apple, offsetx, offsety):
        # Only move the tail if an apple has not been eaten
        # Not moving the tail will result in the snake getting longer
        if grid[head["y"]][head["x"]] != 5:

            # Remember previous tail position so that the used path can be deleted
            previous_tail["x"] = tail["x"]
            previous_tail["y"] = tail["y"]

            # The tail will follow path laid by head
            move_snake_part(grid, tail)

            # Delete used path
            grid[previous_tail["y"]][previous_tail["x"]] = 0
            draw_tile(previous_tail["x"], previous_tail["y"], colors['background'], offsetx, offsety)
            return False
        else:
            # Add new apple in random position. The new position must be empty
            while grid[apple["y"]][apple["x"]] != 0:
                apple["x"] = random.randint(0, grid_size - 1)
                apple["y"] = random.randint(0, grid_size - 1)
            grid[apple["y"]][apple["x"]] = 5
            draw_apple(apple["x"], apple["y"], offsetx, offsety)
            return True


    while True:
        game1 = {}
        game2 = {}
        game1['offsetx'] = 0
        game1['offsety'] = y_padding_size
        game2['offsetx'] = window_size+x_padding_size
        game2['offsety'] = y_padding_size
        # The value inside direction is the direction of the snake head
        # 1 = up, 2 = right, 3 = down, 4 = left
        game1['direction'] = [2]
        game2['direction'] = [2]

        # Start positions
        game1['head'] = {"x": 4, "y": math.floor((grid_size/2))}
        game2['head'] = {"x": 4, "y": math.floor((grid_size/2))}
        game1['tail'] = {"x": game1['head']["x"]-snake_start_length+1, "y": math.floor((grid_size/2))}
        game2['tail'] = {"x": game2['head']["x"]-snake_start_length+1, "y": math.floor((grid_size/2))}
        game1['apple'] = {"x": grid_size-1, "y": math.floor((grid_size/2))}
        game2['apple'] = {"x": grid_size-1, "y": math.floor((grid_size/2))}
        game1['engine'] = ai_engine1(grid_size, game1['head'])
        game2['engine'] = ai_engine2(grid_size, game2['head'])
        game1['color'] = (0, 200, 0)
        game2['color'] = (0, 0, 200)
        game1['previous_tail'] = {"x": 0, "y": 0}  # Used to delete the previous tail position after moving the snake
        game2['previous_tail'] = {"x": 0, "y": 0}
        game1['grid'] = make_grid(game1['offsetx'], game1['offsety'])
        game2['grid'] = make_grid(game2['offsetx'], game2['offsety'])
        game1['score'] = 0
        game2['score'] = 0

        draw_snake_start(game1['grid'], game1['tail'], game1['offsetx'], game1['offsety'], game1['color'])
        draw_snake_start(game2['grid'], game2['tail'], game2['offsetx'], game2['offsety'], game2['color'])
        draw_apple_start(game1['grid'], game1['apple'], game1['offsetx'], game1['offsety'])
        draw_apple_start(game2['grid'], game2['apple'], game2['offsetx'], game2['offsety'])

        turn_number = 0

        def move(game):
            game['direction'].append(game['engine'].get_next_move(game['grid'], game['head'], game['tail'], game['direction'], game['apple']))
            if len(game['direction']) > 1:
                game['direction'].pop(0)
                game['grid'][game['head']["y"]][game['head']["x"]] = game['direction'][0]
            move_snake_part(game['grid'], game['head'])
            if game['head']["x"] < 0 or game['head']["x"] > grid_size-1 or game['head']["y"] < 0 or game['head']["y"] > grid_size-1:
                return False
            apple_collected = move_snake_tail(game['grid'], game['head'], game['previous_tail'], game['tail'], game['apple'], game['offsetx'], game['offsety'])
            if apple_collected:
                game['score'] += 1
            if game['grid'][game['head']["y"]][game['head']["x"]] != 5 and game['grid'][game['head']["y"]][game['head']["x"]] != 0:
                return False
            game['grid'][game['head']["y"]][game['head']["x"]] = game['direction'][0]
            draw_snake(game['head']["x"], game['head']["y"], game['direction'][0], game['offsetx'], game['offsety'], game['color'])
            return True

        status1 = True
        status2 = True

        font = pygame.font.SysFont("Segoe UI", 35)
    
        # Game loop
        while True:
            tick_count += 1
            if tick_count > ticks_per_second/move_speed:
                turn_number += 1
                tick_count = 0
                print('turn_number: ' + str(turn_number), end='\r')
                if status1 == False and status2 == False:
                    event = pygame.event.wait ()
                    if event.type == pygame.QUIT:
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            quit()
                        else:
                            break
                if status1:
                    status1 = move(game1)
                    pygame.draw.rect(screen, (0, 0, 0),
                        (0, 0,
                        window_size, y_padding_size))
                    text = font.render('Moves: ' + str(turn_number), True, (200, 200, 200))
                    text_rect = text.get_rect()
                    text_rect.center = (100, 50)
                    screen.blit(text, text_rect)
                    text = font.render('Apples Gathered: ' + str(game1['score']), True, (200, 200, 200))
                    text_rect = text.get_rect()
                    text_rect.center = (500, 50)
                    screen.blit(text, text_rect)
                if status2:
                    status2 = move(game2)
                    pygame.draw.rect(screen, (0, 0, 0),
                            (window_size+x_padding_size, 0,
                            window_size, y_padding_size))
                    text = font.render('Moves: ' + str(turn_number), True, (200, 200, 200))
                    text_rect = text.get_rect()
                    text_rect.center = (window_size+x_padding_size+100, 50)
                    screen.blit(text, text_rect)
                    text = font.render('Apples Gathered: ' + str(game2['score']), True, (200, 200, 200))
                    text_rect = text.get_rect()
                    text_rect.center = (window_size+x_padding_size+500, 50)
                    screen.blit(text, text_rect)
                pygame.display.update()
            clock.tick(ticks_per_second)
