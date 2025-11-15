# game/ui/player_hud.py
import pygame
from typing import List

from game.assets import config as cfg
from game.assets.graphics import images, shift_hue, resize_image
from game.objects import player as player_module

from game.ui.stacking_icon import StackingIcon as stacking_icon
from game.ui.draining_icon import DrainingIcon as draining_icon

# Bomb cooldown icons (0..8)
_icon_bombs = {}
for i in range(9):
    _icon_bombs.update({i: images[f"bomb_timer_{i}"]})

# Player face icons
_icon_states = {
    "alive": images["icon_player_sigma"],
    "dead": images["icon_player_dead"]
}


class Player_hud:
    """Represents player's in-game HUD"""
    _state_images: List[pygame.Surface] = []

    def __init__(self, position, player: player_module.Player):
        self.position = position
        self.player = player
        self.last_known_state = player.state

        self.hud_image = shift_hue(_icon_states[self.last_known_state], player.hue)

        #Powerup icons (fallback to a known small icon if your key doesn't exist yet)
        speed_icon_surface = images.get("powerup_speedboost") or _icon_bombs[8]
        bomb_range_surface = images.get("powerup_bomb_range") or _icon_bombs[8]
        bomb_cd_surface = images.get("powerup_bomb_cooldown") or _icon_bombs[8]

        self._speed_icon = draining_icon(resize_image(speed_icon_surface, 1), "powerup_speedboost")
        self._range_icon = stacking_icon(resize_image(bomb_range_surface, 1), "powerup_bomb_range")
        self._cooldown_icon = stacking_icon(resize_image(bomb_cd_surface, 1), "powerup_bomb_cooldown")

    def update_hud(self):
        # Swap the face icon when state changes
        if self.last_known_state != self.player.state:
            self.hud_image = shift_hue(_icon_states[self.player.state], self.player.hue)
            self.last_known_state = self.player.state

    def draw(self, surface: pygame.Surface):
        # Background panel
        pygame.draw.rect(surface, "grey", (self.position, cfg.PLAYER_HUD_SIZE))

        # Player face
        surface.blit(self.hud_image, self.position)

        # -------- Bomb cooldown indicator --------
        current_ticks = pygame.time.get_ticks()
        p = self.player
        index = 0

        if p.state == "alive":
            elapsed = current_ticks - p.last_bomb_time
            fraction_done = elapsed / p.bomb_cooldown_ms if p.bomb_cooldown_ms > 0 else 1.0
            fraction_done = min(max(fraction_done, 0), 1)  # Clamp between 0 and 1
            index = int(fraction_done * 8)  # 0..8

        timer_icon = _icon_bombs[index]
        timer_pos = (
            self.position[0] + (self.hud_image.get_width() / 2 - 32),
            self.position[1] + self.hud_image.get_height()
        )
        surface.blit(timer_icon, timer_pos)

        # -------- Speed boost draining icon (reads from effects) --------
        speed_icon_pos = (-999,-999) #just setting a default value off screen so that the actual pos has time to load
        frac = 0.0
        if hasattr(p, "effects"):
            frac = p.effects.fraction_left("speed_boost")

        if speed_icon_pos is (-999,-999): #check if it has been loaded yet, if not (-999,-999) then load it and never do it again
            speed_icon_pos = (
                self.position[0] + self.hud_image.get_width() + 20,  # to the right of the face
                self.position[1] + 10
            )
        self._speed_icon.draw_fraction(surface, speed_icon_pos, frac)
        # ---------------------------------------------------------------
        # -------- Bomb range stacking icon (reads from effects) --------
        bomb_range_pos = (-999,-999)
        stack = 0
        if hasattr(p, "effects"):
            stack = p.effects.stack_count("bomb_range_up")
        
        if bomb_range_pos is (-999,-999):
            bomb_range_pos = (
                self.position[0] + self.hud_image.get_width() + 20,
                self.position[1] + self.hud_image.get_height() + 10
            )
        self._range_icon.draw_stack(surface, bomb_range_pos, stack)
        # ---------------------------------------------------------------
        # -------- Bomb cooldown stacking icon (reads from effects) --------
        bomb_cd_pos = (-999,-999)
        stack = 0
        if hasattr(p, "effects"):
            stack = p.effects.stack_count("bomb_cooldown_reduce")
        
        if bomb_cd_pos is (-999,-999):
            bomb_cd_pos = (
                self.position[0] + self.hud_image.get_width() + 110,
                self.position[1] + 10
            )
        self._cooldown_icon.draw_stack(surface, bomb_cd_pos, stack)
        # ---------------------------------------------------------------