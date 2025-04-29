from game.assets.graphics import images,shift_hue, resize_image
from game.assets import config as cfg

states = {
    "stationary": resize_image(images["player_default"],
                               cfg.TILE_SIZE/ images["player_default"].get_width()),
    "moving": resize_image(images["player_moving"],
                           cfg.TILE_SIZE/ images["player_moving"].get_width()),
    "dead" : resize_image(images["player_dead"], 
                          cfg.TILE_SIZE/ images["player_dead"].get_width())
}



class Player:
    def __init__(self, pos, grid_pos, hue):
        self.state = "stationary"
        self.sprite = shift_hue(states[self.state],hue)
        self.pos = pos
        self.grid_pos = grid_pos

    def draw(self, surface):
        surface.blit(self.sprite, self.pos)


def create_player(pos, grid_pos, hue):
        return Player(
            pos,
            grid_pos,
            hue
        )
    