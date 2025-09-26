from game.assets import config as cfg
from game.objects import powerup as powerup_module

def handle_movement(player, direction, game_grid):
    if player.is_moving:
        return  # Ignore if currently moving

    dx, dy = direction
    new_x = player.grid_pos[0] + dx
    new_y = player.grid_pos[1] + dy

    if not (0 <= new_x < cfg.GRID_WIDTH and 0 <= new_y < cfg.GRID_HEIGHT):
        return

    
    tile_index = new_y * cfg.GRID_WIDTH + new_x # Move y times in 1d grid and take x steps
    target_tile = game_grid[tile_index]  

    if target_tile.obstacle:
        return  # Block movement into obstacle tile
    
    player.grid_pos = (new_x, new_y)
    player.target_pos = (target_tile.pos)
    player.is_moving = True

    if getattr(target_tile, "powerup", None) is not None:
        powerup_module.apply_and_consume(target_tile.powerup, player)
