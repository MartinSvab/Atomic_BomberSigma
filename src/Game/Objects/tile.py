from game.assets import config as cfg
from game.assets import graphics


class Tile:
    tile_sprite = None

    def __init__(self, grid_pos, pixel_pos, obstacle=False):
        if Tile.tile_sprite is None:
            Tile.tile_sprite = graphics.resize_image(
                graphics.images["tile_sprite"],
                cfg.TILE_SIZE / graphics.images["tile_sprite"].get_width()
            )
        self.sprite = Tile.tile_sprite
        self.grid_pos = grid_pos
        self.pos = pixel_pos
        self.obstacle = obstacle
        self.bomb = False
        self.exploding = False
        self.neighbours = [None, None, None, None]  # [R, D, L, U]

    def draw(self, surface):
        surface.blit(self.sprite, self.pos)