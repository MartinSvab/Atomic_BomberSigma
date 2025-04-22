from game.objects.tile import Tile
from game.assets import config as cfg


def create_grid():
    tiles = []
    for row in range(cfg.GRID_HEIGHT):
        for col in range(cfg.GRID_WIDTH):
            x = col * cfg.TILE_SIZE
            y = row * cfg.TILE_SIZE
            tile = Tile((col, row), (x, y))
            tiles.append(tile)

    

    return tiles
