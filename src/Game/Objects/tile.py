from game.assets import config as cfg

class Tile:
    def __init__(self, grid_pos, pixel_pos, obstacle=False):
        self.grid_pos = grid_pos
        self.pos = pixel_pos
        self.obstacle = obstacle
        self.bomb = False
        self.exploding = False
        self.neighbours = [None, None, None, None]  # [R, D, L, U]