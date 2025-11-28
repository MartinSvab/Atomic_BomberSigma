import pygame
from game.assets import config as cfg
from game.systems import input
from game.assets import graphics
from game.ui import button
from game.ui.player_settings_ui import PlayerSettingsUI

def run():
    running = True
    back_to_menu = False

    images = graphics.images
    confirm_button_image = graphics.resize_image(images["confirm_button"], 0.2)

    map_selected = False
    player_settings_done = False
    phase = "map"  # or "players"

    def go_back_to_menu():
        nonlocal running, back_to_menu
        running = False
        back_to_menu = True

    def quit_game():
        nonlocal running, back_to_menu
        running = False
        back_to_menu = False 

    def confirm_map_settings():
        nonlocal map_selected, phase
        map_selected = True
        phase = "players"

    def confirm_player_settings():
        nonlocal player_settings_done, running
        player_settings_done = True
        running = False   # pregame done, move on to game

    buttons_map_selection = [
        button.Button(
            confirm_button_image,
            (cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y + 200),
            confirm_map_settings
        )
    ]
    buttons_player_settings = [
        button.Button(
            confirm_button_image,
            (cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y + 200),
            confirm_player_settings
        )
    ]

    # here later you will create your player settings object
    player_settings_ui = PlayerSettingsUI()  # placeholder

    while running:
        cfg.CLOCK.tick(cfg.FPS)
        input.update_event_queue()

        if input.check_for_quit():
            quit_game()
        if input.check_for_esc():
            go_back_to_menu()

        cfg.DISPLAY.fill((35, 35, 35))

        if phase == "map":
            for event in input._event_list:
                for btn in buttons_map_selection:
                    btn.handle_event(event)

            for btn in buttons_map_selection:
                btn.draw(cfg.DISPLAY)

        elif phase == "players":
            player_settings_ui.handle_events(input._event_list, confirm_player_settings)
            player_settings_ui.draw(cfg.DISPLAY)

            for event in input._event_list:
                for btn in buttons_player_settings:
                    btn.handle_event(event)

            for btn in buttons_player_settings:
                btn.draw(cfg.DISPLAY)

        pygame.display.flip()

    return back_to_menu
