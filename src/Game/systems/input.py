import pygame
from game.systems import movement
from game.assets.keybinds import keybinds

_event_list = []

def update_event_queue():
    global _event_list
    _event_list = pygame.event.get()

def check_for_quit():
    for event in _event_list:
        if event.type == pygame.QUIT:
            return True
    return False

def check_for_esc():
    for event in _event_list:
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False

def check_for_movement_input(player, game_grid):
    keys = pygame.key.get_pressed()
    binds = keybinds[0]  # Only 1 player for now

    if keys[binds[0]]:  # Left
        movement.handle_movement(player, (-1, 0), game_grid)
    elif keys[binds[1]]:  # Down
        movement.handle_movement(player, (0, 1), game_grid)
    elif keys[binds[2]]:  # Right
        movement.handle_movement(player, (1, 0), game_grid)
    elif keys[binds[3]]:  # Up
        movement.handle_movement(player, (0, -1), game_grid)
