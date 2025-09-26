import pygame
from game.assets import config as cfg
from game.assets.graphics import images
from game.systems import input
from game.objects import grid, player
from game.systems import bomb_logic
from game.objects import powerup as powerup_module
from game.ui import player_hud
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

    #Create grid
    game_grid = grid.create_grid()
    bombs: list = []

    #Create players
    player_list = []
    for p in range(cfg.LOCAL_PLAYERS):
        random_hue = random.uniform(0, 1)
        random_tile = game_grid[random.randint(0, len(game_grid) - 1)]
        player_list.append(
            player.create_player(random_tile.pos, random_tile.grid_pos, random_hue, p)
        )
        player_list[p].hud = player_hud.Player_hud((cfg.PLAYER_HUD_MARGIN,cfg.PLAYER_HUD_MARGIN + (p * 250)),player_list[p])

    while running:
        cfg.CLOCK.tick(cfg.FPS)
        input.update_event_queue()

        if input.check_for_quit():
            quit_game()

        if input.check_for_esc():
            go_back_to_menu()

        cfg.DISPLAY.fill((35, 35, 35))

        grid.draw_grid(game_grid, cfg.DISPLAY)

        #draw all powerups, update all player effects
        powerup_module.draw_all(cfg.DISPLAY)
        powerup_module.update_effects()

        # handle everything player related
        for p in range(cfg.LOCAL_PLAYERS):
            player_state = getattr(player_list[p],"state")
            if(player_state != "dead"):
                input.check_for_movement_input(player_list[p], game_grid)
                bomb_logic.handle_bomb_input(player_list[p], bombs, game_grid)
            player_list[p].draw(cfg.DISPLAY)
            

        # update and draw bombs
        bomb_logic.update_bombs(bombs, game_grid, player_list)
        bomb_logic.draw_bombs(bombs, cfg.DISPLAY)

        pygame.display.flip()

    return should_quit