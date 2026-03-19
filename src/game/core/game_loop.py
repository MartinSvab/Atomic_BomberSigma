import pygame
from concurrent.futures import ThreadPoolExecutor
from game.assets import config as cfg
from game.assets.graphics import images, shift_hue
from game.systems import input
from game.objects import grid, player
from game.systems import bomb_logic
from game.objects import powerup as powerup_module
from game.ui import player_hud, pause_menu, moving_element
import random


def _preload_player_assets_async(players):
    """Precompute hue-shifted sprites/HUD icons off the main thread."""
    if not players:
        return

    def build(player_obj):
        try:
            # Preload board sprites
            preloaded = {
                "alive": shift_hue(player.states["alive"], player_obj.hue),
                "dead": shift_hue(player.states["dead"], player_obj.hue),
            }
            player_obj.preloaded_sprites = preloaded
            # Ensure current sprite uses cached version
            player_obj.sprite = preloaded.get(player_obj.state, player_obj.sprite)

            # Preload HUD icons if HUD exists
            if getattr(player_obj, "hud", None):
                player_obj.hud.preload_icons()
        except Exception:
            # Silently continue; runtime fallback will handle it
            pass

    # Cap workers to avoid excessive threads; at least 2
    workers = max(2, min(8, len(players)))
    executor = ThreadPoolExecutor(max_workers=workers)
    for p in players:
        executor.submit(build, p)
    # Do not wait; allow game to continue while preloading
    executor.shutdown(wait=False)

def run():
    running = True
    should_quit = False
    should_restart = False
    paused = False
    game_end = False

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
    
    #Pregenerate game end texts/images
    game_over_text = moving_element.MovingElement(images["game_over_text"], 
                                                  (cfg.DISPLAY_CENTER_X, -500),  #using 500 as a random number outside the rendering range
                                                  (cfg.DISPLAY_CENTER_X, 128),   #also the same reason for the other 500s in the other moving elements
                                                  600)
    winner_text = moving_element.MovingElement(images["win_text"], 
                                                  (cfg.DISPLAY_CENTER_X, cfg.DISPLAY.get_height()+500), 
                                                  (cfg.DISPLAY_CENTER_X, cfg.DISPLAY.get_height()-128), 
                                                  600)
    winner_arrow = moving_element.WinnerArrow(
    images["shiftable_arrow"],
    600
)

    #Create grid
    def build_match_grid():
        selected_preset = cfg.SELECTED_MAP if cfg.SELECTED_MAP != "random" else None
        obstacle_chance = cfg.RANDOM_MAP_OBSTACLE_CHANCE if cfg.SELECTED_MAP == "random" else None

        for _ in range(40):
            generated_grid = grid.create_grid(selected_preset, obstacle_chance=obstacle_chance)
            if len(grid.get_spawnable_tiles(generated_grid)) >= cfg.LOCAL_PLAYERS:
                return generated_grid

        generated_grid = grid.create_grid(selected_preset, obstacle_chance=obstacle_chance)
        candidate_tiles = generated_grid[:]
        random.shuffle(candidate_tiles)
        for tile in candidate_tiles[:cfg.LOCAL_PLAYERS]:
            grid.carve_spawn_lane(generated_grid, tile)
        return generated_grid

    game_grid = build_match_grid()
    bombs: list = []

    #stuff for game end animations
    match_winner = None
    winner_text_variants = {}
    winner_arrow_variants = {}

    #Create players
    player_list = []
    alive_players = []
    spawnable_tiles = grid.get_spawnable_tiles(game_grid)
    available_spawn_tiles = spawnable_tiles[:] if len(spawnable_tiles) >= cfg.LOCAL_PLAYERS else [
        tile for tile in game_grid if not tile.obstacle
    ]

    for p in range(cfg.LOCAL_PLAYERS):
        configured_hues = getattr(cfg, "PLAYER_HUES", [])
        random_hue = configured_hues[p] if p < len(configured_hues) else random.uniform(0, 1)
        if not available_spawn_tiles:
            available_spawn_tiles = [tile for tile in game_grid if not tile.obstacle]
        random_tile = random.choice(available_spawn_tiles)
        available_spawn_tiles.remove(random_tile)
        new_player = player.create_player(random_tile.pos, random_tile.grid_pos, random_hue, p)
        player_list.append(new_player)
        alive_players.append(new_player)
        player_list[p].hud = player_hud.Player_hud((cfg.PLAYER_HUD_MARGIN,cfg.PLAYER_HUD_MARGIN + (p * 250)),player_list[p])

    for p in player_list:
        winner_text_variants[p] = shift_hue(images["win_text"], p.hue)

    for p in player_list:
        winner_arrow_variants[p] = shift_hue(images["shiftable_arrow"], p.hue)

    # Preload hue-shifted sprites and HUD icons asynchronously to avoid runtime lag
    _preload_player_assets_async(player_list)

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
        if not paused and not game_end:
            #bombs
            killed_players_tt = bomb_logic.update_bombs(bombs, game_grid, player_list)

            #players
            for p in range(cfg.LOCAL_PLAYERS):
                player_state = getattr(player_list[p],"state")
                if player_state != "dead":
                    input.check_for_movement_input(player_list[p], game_grid)
                    bomb_logic.handle_bomb_input(player_list[p], bombs, game_grid)
                if player_list[p] in killed_players_tt:
                    alive_players.remove(player_list[p])
                    player_list[p].tod = pygame.time.get_ticks()
                    

            #game end check
            match len(alive_players):
                case 0:
                    winner_text.set_image(images["lose_text"])
                    winner_arrow_variants.clear() #clear to save memory since we won't be using them
                    game_end = True
                case 1:
                    match_winner = alive_players[0]
                    winner_text.set_image(winner_text_variants[match_winner])
                    winner_arrow.configure(
                        winner_text,
                        match_winner,
                        winner_arrow_variants[match_winner]
                    )
                    game_end = True
                case _:
                    pass


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
            pause_action = pm.pause()
            pause_elapsed = pygame.time.get_ticks() - pause_started
            paused = False

            # keep cooldowns/effects from expiring during pause
            if pause_elapsed > 0:
                for p in player_list:
                    p.last_bomb_time += pause_elapsed
                    if hasattr(p, "effects"):
                        p.effects.apply_time_offset(pause_elapsed)

            if pause_action == "menu":
                running = False
            elif pause_action == "quit":
                quit_game()
            elif pause_action == "restart":
                should_restart = True
                running = False

            if not running:
                continue


        #Finishing animations when there is one or zero players alive
        if game_end:
            bombs.clear()

            dt = cfg.CLOCK.get_time()

            finished1 = game_over_text.update(dt)
            game_over_text.draw(cfg.DISPLAY)

            if finished1:
                if match_winner:
                    winner_arrow.update(dt)
                    winner_arrow.draw(cfg.DISPLAY)

                winner_text.update(dt)
                winner_text.draw(cfg.DISPLAY)




        #render
        pygame.display.flip()
        




    if should_restart:
        return "restart"

    return should_quit
