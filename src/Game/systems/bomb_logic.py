"""
Bomb logic helpers for Atomic BomberSigma.

This module handles bomb placement input, updates active bombs and draws them.
"""

import pygame
from typing import List

from game.assets import keybinds
from game.assets import config as cfg
from game.objects.bomb import Bomb
from game.systems import input as input_sys

def handle_bomb_input(player, bombs: List[Bomb], game_grid) -> None:
    """
    Check the event queue for a space‑bar press and place a bomb on the player's tile.
    """
    for event in input_sys._event_list:
        if event.type == pygame.KEYDOWN and event.key == keybinds.keybinds[player.player_index][4] and player.can_place_bomb():
            col, row = player.grid_pos
            tile_index = row * cfg.GRID_WIDTH + col
            tile = game_grid[tile_index]
            if not tile.bomb:
                bombs.append(Bomb(tile, (col, row)))
                player.last_bomb_time = pygame.time.get_ticks()
            break

def update_bombs(bombs: List[Bomb], game_grid, players) -> None:
    """
    Tick all bombs and remove any that are finished exploding.
    """
    finished = []
    for bomb in bombs:
        if bomb.update(game_grid, players):
            finished.append(bomb)
    for b in finished:
        bombs.remove(b)

def draw_bombs(bombs: List[Bomb], surface) -> None:
    """
    Draw all bombs and explosion animations.
    """
    for bomb in bombs:
        bomb.draw(surface)
