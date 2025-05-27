from game.assets import config as cfg

def handle_movement(player, direction):
    if player.is_moving:
        return  # Ignore if currently moving

    dx, dy = direction
    new_x = player.grid_pos[0] + dx
    new_y = player.grid_pos[1] + dy

    if 0 <= new_x < cfg.GRID_WIDTH and 0 <= new_y < cfg.GRID_HEIGHT:
        player.grid_pos = (new_x, new_y)
        player.target_pos = (
            new_x * cfg.TILE_SIZE + cfg.GRID_X_POS,
            new_y * cfg.TILE_SIZE + cfg.GRID_Y_POS
        )
        player.moving = True
