"""
Powerup.py is a module that hosts logic for creating and managing powerups in game,
by assigning them to a tile with create_powerup(tile) and then, if a player picks them up
makes sure to apply the powerup efffect to the player
"""

from game.objects import tile as tile_module
from game.objects import player as player_module


class Powerup:
    _powerup_types=[
        "speed_boost":""
    ]
    

    def __init__(self, tile:tile_module):
        