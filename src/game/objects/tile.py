# game/objects/tile.py
from game.assets import config as cfg
from game.assets import graphics


class Tile:
    empty_tile_sprite = None
    obstacle_tile_sprite = None

    def __init__(self, grid_pos, pixel_pos, obstacle=False):
        if Tile.empty_tile_sprite is None:
            Tile.empty_tile_sprite = graphics.resize_image(
                graphics.images["tile_sprite"],
                cfg.TILE_SIZE / graphics.images["tile_sprite"].get_width()
            )
        if Tile.obstacle_tile_sprite is None:
            Tile.obstacle_tile_sprite = graphics.resize_image(
                graphics.images["obstacle_sprite"],
                cfg.TILE_SIZE / graphics.images["obstacle_sprite"].get_width()
            )

        self.sprite = Tile.obstacle_tile_sprite if obstacle else Tile.empty_tile_sprite

        self.grid_pos = grid_pos
        self.pos = pixel_pos
        self.obstacle = obstacle
        self.bomb = False
        self.exploding = False
        self.spawn_tile = False
        self.neighbours = [None, None, None, None]

        self.powerup = None

    def draw(self, surface):
        # base tile
        surface.blit(self.sprite, self.pos)

        # draw powerup on top if present
        if self.powerup and hasattr(self.powerup, "icon"):
            surface.blit(self.powerup.icon, self.pos)
