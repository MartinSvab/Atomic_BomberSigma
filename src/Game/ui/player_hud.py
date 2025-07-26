import pygame
from typing import List

from game.assets import config as cfg
from game.assets.graphics import images, shift_hue, resize_image
from game.objects import player

_icon_bombs = {}
for i in range(9):
    _icon_bombs.update({i:images[f"bomb_timer_{i}"]})

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
        self.last_known_state = player.state

        self.hud_image = shift_hue(_icon_states[self.last_known_state],player.hue)

    def update_hud(self):
        if self.last_known_state is not self.player.state: 
            self.hud_image = shift_hue(_icon_states[self.player.state],self.player.hue)
            self.last_known_state = self.player.state
        else: 
            print(self.last_known_state, self.player.state)

    def draw(self, surface:pygame.Surface):
        #First, draw a grey rectangle underneath the HUD itself
        pygame.draw.rect(surface, "grey", (self.position, cfg.PLAYER_HUD_SIZE))
        
        #Then add the player icon
        surface.blit(self.hud_image,self.position)

        #Then, add other stats into the window, such as bomb delay and bomb range
        #=========bomb cooldown==========
        current_ticks = pygame.time.get_ticks()
        player = self.player
        index = 0

        if player.state == "alive":
            elapsed = current_ticks - player.last_bomb_time
            fraction_done = elapsed / player.bomb_cooldown_ms if player.bomb_cooldown_ms > 0 else 1.0
            fraction_done = min(max(fraction_done, 0), 1)  # Clamp between 0 and 1

            # Calculate which icon to show
            index = int(fraction_done * 8)  # 0 = done, 8 = just placed

        # Draw the timer icon next to the player face icon
        timer_icon = _icon_bombs[index]
        timer_pos = (self.position[0] + (self.hud_image.get_width()/2 - 32), self.position[1] + self.hud_image.get_height())  # Offset from face

        surface.blit(timer_icon, timer_pos)