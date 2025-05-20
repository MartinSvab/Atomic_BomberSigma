import pygame
from game.assets import config as cfg
from game.assets.graphics import images
from game.systems import input
from game.objects import grid, player
import random

def run():
    running = True
    should_quit = False

    def go_back_to_menu():
        nonlocal running
        running = False

    def quit_game():
        nonlocal running
        running = False 
        nonlocal should_quit
        should_quit = True


    game_grid = grid.create_grid() # create grid


    player_list = []
    for p in range(cfg.LOCAL_PLAYERS):
        random_hue = random.uniform(0,1)
        random_tile = game_grid[random.randint(0,len(game_grid) - 1)]
        player_list.append(player.create_player(random_tile.pos, random_tile.grid_pos, random_hue))


    while running:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates the event queue

        if input.check_for_quit():
            quit_game()

        if input.check_for_esc():
            go_back_to_menu()


        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)


        grid.draw_grid(game_grid,cfg.DISPLAY) # Display grid

        for p in range(cfg.LOCAL_PLAYERS): 
            player_list[p].draw(cfg.DISPLAY) # Draws players
            input.check_for_movement_input() # Checks for movement for each player

        pygame.display.flip() # Flip the display (Render everything)
    
    return should_quit