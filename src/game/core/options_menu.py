import pygame
from game.assets.keybinds import keybinds
import game.assets.config as cfg
from game.assets import graphics
from game.systems import input
from game.ui import button

font = pygame.font.SysFont(None, 24)

def run():
    in_menu = True
    should_quit = False
    player_count = cfg.LOCAL_PLAYERS

    images = graphics.images
    return_button_image = graphics.resize_image(images["return_button"], 1)

    kb_icons = {
        "left":  images["keybind_left"],
        "up":    images["keybind_up"],
        "right": images["keybind_right"],
        "down":  images["keybind_down"],
        "bomb": images["keybind_bomb"]
    }
    directions = ["left", "up", "right", "down", "bomb"]

    # Which (player, direction) is currently waiting for a new key?
    editing_bind = None  # tuple[int, str] | None

    # Ensure keybinds list is long enough for current player_count
    def ensure_keybinds_length(n_players: int):
        # Expecting keybinds like: [[left, up, right, down], ...]
        default_row = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]
        while len(keybinds) < n_players:
            keybinds.append(default_row.copy())
        # If there are too many rows, we don't delete them—just ignore extra players

    ensure_keybinds_length(player_count)

    # Build all buttons (main controls + per-player keybinds)
    def build_buttons():
        bind_buttons = []

        start_x, start_y = 220, 220
        step_x, step_y   = 150, 120

        for p in range(player_count):
            for d_i, d in enumerate(directions):
                img = kb_icons[d]
                pos = (start_x + d_i * step_x, start_y + p * step_y)

                def make_action(player_index, direction_name):
                    def action():
                        nonlocal editing_bind
                        editing_bind = (player_index, direction_name)
                    return action

                b = button.Button(img, pos, make_action(p, d), label=d)
                # Attach metadata so we always know who this belongs to
                b.meta = {"player": p, "direction": d}
                bind_buttons.append(b)

        main_buttons = [
            button.Button(
                return_button_image,
                (return_button_image.get_width() / 2, return_button_image.get_height() / 2),
                lambda: _return_to_main_menu()
            ),
            button.Button(images["plus_button"],  (1000, 640), lambda: _increase_player_count()),
            button.Button(images["minus_button"], (1100, 640), lambda: _decrease_player_count()),
        ]

        return main_buttons + bind_buttons

    # These are small thunks so build_buttons can capture them
    def _return_to_main_menu():
        nonlocal in_menu
        in_menu = False

    def _quit_game():
        nonlocal in_menu, should_quit
        in_menu = False
        should_quit = True

    def _increase_player_count():
        nonlocal player_count, buttons
        if player_count < 4:
            player_count += 1
            ensure_keybinds_length(player_count)
            buttons = build_buttons()

    def _decrease_player_count():
        nonlocal player_count, buttons, editing_bind
        if player_count > 1:
            # If we were editing a bind of a player that’s going to disappear, cancel it
            if editing_bind is not None and editing_bind[0] == player_count - 1:
                editing_bind = None
            player_count -= 1
            buttons = build_buttons()

    buttons = build_buttons()

    while in_menu:
        cfg.CLOCK.tick(cfg.FPS)
        input.update_event_queue()

        for event in input._event_list:
            if event.type == pygame.QUIT:
                _quit_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and editing_bind is None:
                _return_to_main_menu()

            # Handle rebinding: if we're waiting for a key, take the next KEYDOWN
            if editing_bind is not None and event.type == pygame.KEYDOWN:
                p_i, direction = editing_bind
                if 0 <= p_i < player_count:
                    idx = directions.index(direction)
                    keybinds[p_i][idx] = event.key  # store new keycode
                editing_bind = None

        
        for event in input._event_list:
            for btn in buttons:
                btn.handle_event(event)


        # ================== RENDER ==================
        cfg.DISPLAY.fill((35, 35, 35))

        for btn in buttons:
            btn.draw(cfg.DISPLAY)


            # Draw the key name (or "..." if this one is being edited)
            if hasattr(btn, "meta"):  # only for keybind buttons
                p = btn.meta["player"]
                d = btn.meta["direction"]
                if editing_bind is not None and editing_bind == (p, d):
                    text_label = "..."
                else:
                    idx = directions.index(d)
                    # Guard: if keybinds shrank somehow, show blank
                    if p < len(keybinds) and idx < len(keybinds[p]):
                        text_label = pygame.key.name(keybinds[p][idx])
                    else:
                        text_label = ""

                if text_label:
                    text_surf = font.render(text_label, True, "white")
                    cfg.DISPLAY.blit(
                        text_surf,
                        (btn.rect.centerx - text_surf.get_width() / 2,
                         btn.rect.bottom + 6)
                    )

        pygame.display.flip()

    cfg.LOCAL_PLAYERS = player_count
    return should_quit
