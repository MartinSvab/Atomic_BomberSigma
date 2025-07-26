import pygame #stupid import ik but its the cleanest solution i found for the bomb stuff
from game.assets.graphics import images,shift_hue, resize_image
from game.assets import config as cfg
import time

states = {
    "alive": resize_image(images["player_default"],
                               cfg.TILE_SIZE/ images["player_default"].get_width()),
    "dead" : resize_image(images["player_dead"], 
                          cfg.TILE_SIZE/ images["player_dead"].get_width())
}



class Player:
    """Represents the player's in-game on-board sprite"""
    def __init__(self, pos, grid_pos, hue):
        self.state = "alive"
        self.hue = hue
        self.sprite = shift_hue(states["alive"],hue)
        self.pos = pos
        self.grid_pos = grid_pos
        self.target_pos = pos  # where to move toward
        self.is_moving = False
        self.hud = None
        self.last_bomb_time = 0  #Last tick a bomb was placed


        #Stats
        self.move_speed = 8  # pixels per frame (adjust for smoothness)
        self.bomb_cooldown_ms = cfg.DEFAULT_BOMB_COOLDOWN

    def update_sprite(self):
        self.sprite = shift_hue(states[self.state], self.hue)
        self.hud.update_hud()

    def draw(self, surface):
        if self.is_moving:
            # Move current position toward target position
            x, y = self.pos
            tx, ty = self.target_pos

            dx = tx - x
            dy = ty - y

            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist <= self.move_speed:
                self.pos = self.target_pos
                self.is_moving = False
            else:
                step_x = self.move_speed if dx > 0 else -self.move_speed
                step_y = self.move_speed if dy > 0 else -self.move_speed

                # Only move in direction of need
                if abs(dx) > self.move_speed:
                    x += step_x
                else:
                    x = tx
                if abs(dy) > self.move_speed:
                    y += step_y
                else:
                    y = ty

                self.pos = (x, y)

        surface.blit(self.sprite, self.pos)
        self.hud.draw(surface)

    def can_place_bomb(self):
        return pygame.time.get_ticks() - self.last_bomb_time >= self.bomb_cooldown_ms




def create_player(pos, grid_pos, hue):
        return Player(
            pos,
            grid_pos,   
            hue
        )
    