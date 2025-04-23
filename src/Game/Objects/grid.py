from game.objects.tile import Tile
from game.assets import config as cfg


def create_grid():
    x_offset = (cfg.SCREEN_WIDTH  - cfg.GRID_WIDTH  * cfg.TILE_SIZE) // 2
    y_offset = (cfg.SCREEN_HEIGHT - cfg.GRID_HEIGHT * cfg.TILE_SIZE) // 2
    tiles = []
    
    for row in range(cfg.GRID_HEIGHT):
        for col in range(cfg.GRID_WIDTH):
            x = col * cfg.TILE_SIZE + x_offset
            y = row * cfg.TILE_SIZE + y_offset
            tile = Tile((col, row), (x, y))
            tiles.append(tile)

    assign_neighbors(tiles, cfg.GRID_WIDTH, cfg.GRID_HEIGHT)
    

    return tiles

def draw_grid(tiles:list[Tile], surface):
    for tile in tiles:
        tile.draw(surface)



def assign_neighbors(tiles:list[Tile], grid_width, grid_height):
    for tile in tiles:
        col, row = tile.grid_pos

        directions = [
            (1, 0),   # right
            (0, 1),   # down
            (-1, 0),  # left
            (0, -1)   # up
        ]

        tile.neighbors = []

        for dx, dy in directions:
            nx, ny = col + dx, row + dy

            # Check if neighbor is within bounds
            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                neighbor_index = ny * grid_width + nx
                tile.neighbors.append(tiles[neighbor_index])
            else:
                tile.neighbors.append(None)