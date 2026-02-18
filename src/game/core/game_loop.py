import pygame
from game.assets import config as cfg
from game.assets.graphics import images
from game.systems import input
from game.objects import grid, player
from game.systems import bomb_logic
from game.objects import powerup as powerup_module
from game.ui import player_hud, pause_menu
import random

def run():
    running = True
    should_quit = False
    paused = False

    def pause_game():
        nonlocal paused
        if paused == False:
            paused = True
        else:
            paused = False
    
    def go_back_to_menu():
        nonlocal running
        running = False

    def quit_game():
        nonlocal running
        running = False
        nonlocal should_quit
        should_quit = True

    #Pregenerate pause menu
    pm = pause_menu.Pause_menu(cfg.DISPLAY)

    #Create grid
    game_grid = grid.create_grid()
    bombs: list = []

    #Create players
    player_list = []
    alive_players = []
    used_tiles = []
    for p in range(cfg.LOCAL_PLAYERS):
        random_hue = random.uniform(0, 1)
        while True:
            random_tile = game_grid[random.randint(0, len(game_grid) - 1)]
            if not random_tile.obstacle and random_tile not in used_tiles:
                break
        player_list.append(
            player.create_player(random_tile.pos, random_tile.grid_pos, random_hue, p)
        )
        player_list[p].hud = player_hud.Player_hud((cfg.PLAYER_HUD_MARGIN,cfg.PLAYER_HUD_MARGIN + (p * 250)),player_list[p])
        used_tiles.append(random_tile)

    #=====MAIN GAME LOOP======
    while running:
        cfg.CLOCK.tick(cfg.FPS)

        #=INPUT=
        input.update_event_queue()

        if input.check_for_quit():
            quit_game()

        if input.check_for_esc():
            pause_game()


        #=LOGIC=
        if not paused:
            #bombs
            bomb_logic.update_bombs(bombs, game_grid, player_list)

            #players
            for p in range(cfg.LOCAL_PLAYERS):
                player_state = getattr(player_list[p],"state")
                if(player_state != "dead"):
                    input.check_for_movement_input(player_list[p], game_grid)
                    bomb_logic.handle_bomb_input(player_list[p], bombs, game_grid)

            
                


        #=RENDERING=
        #bg
        cfg.DISPLAY.fill((35, 35, 35)) 

        #grid
        grid.draw_grid(game_grid, cfg.DISPLAY) 

        #players
        for p in range(cfg.LOCAL_PLAYERS): 
            player_list[p].draw(cfg.DISPLAY)

        #bombs
        bomb_logic.draw_bombs(bombs, cfg.DISPLAY) 

        #pause menu
        if paused:
            pause_started = pygame.time.get_ticks()
            cont = pm.pause()
            pause_elapsed = pygame.time.get_ticks() - pause_started
            paused = False

            # keep cooldowns/effects from expiring during pause
            if pause_elapsed > 0:
                for p in player_list:
                    p.last_bomb_time += pause_elapsed
                    if hasattr(p, "effects"):
                        p.effects.apply_time_offset(pause_elapsed)

            if not cont:
                running = False


        #render
        pygame.display.flip()
        

    return should_quit
