import pygame
from game.assets import config as cfg
from game.systems import input
from game.assets import graphics
from game.ui import button
from game.ui.player_settings_ui import PlayerSettingsUI
from game.ui.map_selection_ui import MapSelectionUI

def run():
    running = True
    back_to_menu = False

    images = graphics.images
    confirm_button_image = graphics.resize_image(images["confirm_button"], 0.2)

    def go_back_to_menu():
        nonlocal running, back_to_menu
        running = False
        back_to_menu = True

    def quit_game():
        nonlocal running, back_to_menu
        running = False
        back_to_menu = False

    # phase UIs
    map_ui = MapSelectionUI()
    players_ui = PlayerSettingsUI()

    phase = "map"
    current_ui = map_ui

    def confirm_current():
        nonlocal running, phase, current_ui
        current_ui.confirm()

        if phase == "map":
            phase = "players"
            current_ui = players_ui
        else:
            running = False

    confirm_btn = button.Button(
        confirm_button_image,
        (cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y + 400),
        confirm_current
    )

    # allow PlayerSettingsUI to trigger the same confirm flow (e.g. Enter key)
    players_ui.on_confirm = confirm_current

    while running:
        cfg.CLOCK.tick(cfg.FPS)
        input.update_event_queue()

        if input.check_for_quit():
            quit_game()
        if input.check_for_esc():
            go_back_to_menu()

        cfg.DISPLAY.fill((35, 35, 35))

        current_ui.handle_events(input._event_list)
        current_ui.draw(cfg.DISPLAY)

        for e in input._event_list:
            confirm_btn.handle_event(e)
        confirm_btn.draw(cfg.DISPLAY)

        pygame.display.flip()

    return back_to_menu
