import pygame
from typing import List

from game.assets import config as cfg
from game.assets.graphics import images, shift_hue, resize_image
from game.objects import player

_icon_states = {
    "alive": images["icon_player_sigma"],
    "dead": images["icon_player_dead"]
}

class Player_hud:
    """Represents player's in-game HUD"""

    _state_images: List[pygame.Surface] = []

    def __init__(self, position, player:player.Player):
        self.position = position
        self.player = player

        self.hud_image = shift_hue(_icon_states[player.state],player.hue)



    def draw(self, surface:pygame.Surface):
        #First, draw a grey rectangle underneath the HUD itself
        pygame.draw.rect(surface, "red", (self.position, cfg.PLAYER_HUD_SIZE))