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
    return_button_image = graphics.resize_image(images["return_button"],1)

    kb = {  # Keybinding icons
        "left":  images["keybind_left"],
        "up":    images["keybind_up"],
        "right": images["keybind_right"],
        "down":  images["keybind_down"]
    }

    directions = ["left", "up", "right", "down"]
    editing_bind = None  # (index, direction)

    bind_buttons = []
    for idx, direction in enumerate(directions):
        img = kb[direction]
        pos = (200 + idx * 150, 400)  # layout horizontally for now

        def make_action(i, d):
            def action():
                nonlocal editing_bind
                editing_bind = (0, d)  # (player_index, direction)
            return action

        bind_buttons.append(
            button.Button(img, pos, make_action(idx, direction), label=direction)
        )

    def return_to_main_menu():
        nonlocal in_menu
        in_menu = False

    def quit_game():
        nonlocal in_menu, should_quit
        in_menu = False 
        should_quit = True

    def increase_player_count():
        nonlocal player_count
        if player_count < 4:
            player_count += 1
    
    def decrease_player_count():
        nonlocal player_count
        if player_count > 1:
            player_count -= 1

    buttons = [
        button.Button(return_button_image,
                      (0 + return_button_image.get_width()/2,
                       0 + return_button_image.get_height()/2),
                      return_to_main_menu),
        button.Button(images["plus_button"], (1000,640), increase_player_count),
        button.Button(images["minus_button"], (1100,640), decrease_player_count)
    ] + bind_buttons

    while in_menu:
        cfg.CLOCK.tick(cfg.FPS)
        input.update_event_queue()

        for event in input._event_list:
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and editing_bind is None:
                return_to_main_menu()

            # rebinding
            if editing_bind is not None and event.type == pygame.KEYDOWN:
                p_i, direction = editing_bind
                idx = directions.index(direction)
                keybinds[p_i][idx] = event.key  # store new keycode

                # update label text on the correct button
                for b in bind_buttons:
                    if b.label == direction or b.label == "...":
                        b.label = pygame.key.name(event.key)
                editing_bind = None

        # ================== RENDER ==================
        cfg.DISPLAY.fill((35,35,35))

        for btn in buttons:
            btn.draw(cfg.DISPLAY)
            if btn.is_clicked():
                if btn.label in directions:  # only set to "..." when valid
                    btn.label = "..."
                btn.perform_action()

            # draw key name under button
            text_label = btn.label if btn.label == "..." else ""
            if btn.label in directions:
                idx = directions.index(btn.label)
                text_label = pygame.key.name(keybinds[0][idx])

            if text_label:
                text_surf = font.render(text_label, True, "white")
                cfg.DISPLAY.blit(text_surf,
                    (btn.rect.centerx - text_surf.get_width()/2,
                     btn.rect.bottom + 5))

        pygame.display.flip()

    cfg.LOCAL_PLAYERS = player_count
    return should_quit
