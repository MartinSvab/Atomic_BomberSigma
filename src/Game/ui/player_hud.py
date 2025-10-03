# game/ui/player_hud.py
import pygame
from typing import List

from game.assets import config as cfg
from game.assets.graphics import images, shift_hue, resize_image
from game.objects import player as player_module

# Bomb cooldown icons (0..8)
_icon_bombs = {}
for i in range(9):
    _icon_bombs.update({i: images[f"bomb_timer_{i}"]})

# Player face icons
_icon_states = {
    "alive": images["icon_player_sigma"],
    "dead": images["icon_player_dead"]
}

class DrainingIcon:
    """Draw a surface cropped from top->bottom by fraction_left (0..1)."""
    def __init__(self, icon_surface: pygame.Surface):
        self.icon = icon_surface

    def draw_fraction(self, surface: pygame.Surface, pos: tuple[int, int], fraction_left: float):
        f = max(0.0, min(1.0, float(fraction_left)))
        if f <= 0:
            return
        full_w = self.icon.get_width()
        full_h = self.icon.get_height()
        vis_h = int(full_h * f)
        # keep bottom visible, cut from top
        src = pygame.Rect(0, full_h - vis_h, full_w, vis_h)
        dest = (pos[0], pos[1] + (full_h - vis_h))
        surface.blit(self.icon, dest, src)

class Player_hud:
    """Represents player's in-game HUD"""
    _state_images: List[pygame.Surface] = []

    def __init__(self, position, player: player_module.Player):
        self.position = position
        self.player = player
        self.last_known_state = player.state

        self.hud_image = shift_hue(_icon_states[self.last_known_state], player.hue)

        # Speed icon (fallback to a known small icon if your key doesn't exist yet)
        speed_icon_surface = images.get("powerup_speedboost") or _icon_bombs[8]
        self._speed_icon = DrainingIcon(resize_image(speed_icon_surface, 1))

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
        frac = 0.0
        if hasattr(p, "effects"):
            frac = p.effects.fraction_left("speed_boost")

        if frac > 0.0:
            speed_icon_pos = (
                self.position[0] + self.hud_image.get_width() + 20,  # to the right of the face
                self.position[1] + 10
            )
            self._speed_icon.draw_fraction(surface, speed_icon_pos, frac)
        # ---------------------------------------------------------------
