"""
This module defines a simple Bomb class for the Atomic BomberSigma project.

A Bomb is placed on a tile in the grid when a player presses the bomb key.
It counts down for a short period and then explodes in a cross pattern,
destroying obstacles and killing players caught in its blast.
"""

import pygame
from typing import List, Tuple

from game.assets import config as cfg
from game.assets import graphics
from game.objects import tile as tile_module
from game.objects import player as player_module


class Bomb:
    """Represents a bomb placed by a player."""

    _stage_images: List[pygame.Surface] = []
    _explosion_horizontal: pygame.Surface = None
    _explosion_vertical: pygame.Surface = None

    def __init__(self, tile: tile_module.Tile, grid_pos: Tuple[int, int],
                 radius: int = 1, fuse_frames: int = 120) -> None:
        self.tile = tile
        self.grid_pos = grid_pos
        self.radius = radius
        self.fuse_frames = fuse_frames
        self._frame_counter = 0
        self.exploded = False
        self.explosion_frames_remaining = 30
        self.explosion_tiles: List[tile_module.Tile] = []
        # Mark the tile as containing a bomb
        self.tile.bomb = True
        # Load assets once
        if not Bomb._stage_images:
            self._load_assets()

    @classmethod
    def _load_assets(cls) -> None:
        images = graphics.images
        # Bomb animation frames
        for i in range(1, 6):
            img_key = f"bomb_stage_{i}"
            if img_key in images:
                ratio = cfg.TILE_SIZE / images[img_key].get_width()
                cls._stage_images.append(
                    graphics.resize_image(images[img_key], ratio)
                )
        # Explosion sprites
        if "bomb_explosion_horizontal" in images:
            ratio_h = cfg.TILE_SIZE / images["bomb_explosion_horizontal"].get_width()
            cls._explosion_horizontal = graphics.resize_image(images["bomb_explosion_horizontal"], ratio_h)
        if "bomb_explosion_vertical" in images:
            ratio_v = cfg.TILE_SIZE / images["bomb_explosion_vertical"].get_width()
            cls._explosion_vertical = graphics.resize_image(images["bomb_explosion_vertical"], ratio_v)

    def update(self, game_grid: List[tile_module.Tile], players: List[player_module.Player]) -> bool:
        """
        Tick the fuse or count down the explosion animation.
        Returns True when the bomb has finished exploding and should be removed.
        """
        if not self.exploded:
            self._frame_counter += 1
            if self._frame_counter >= self.fuse_frames:
                self._explode(game_grid, players)
        else:
            self.explosion_frames_remaining -= 1
            if self.explosion_frames_remaining <= 0:
                for t in self.explosion_tiles:
                    t.exploding = False
                self.tile.bomb = False
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the bomb sprite or its explosion onto the surface.
        """
        if not self.exploded:
            if self.fuse_frames > 0 and Bomb._stage_images:
                stage_index = min(
                    len(Bomb._stage_images) - 1,
                    (self._frame_counter * len(Bomb._stage_images)) // self.fuse_frames
                )
            else:
                stage_index = 0
            image = Bomb._stage_images[stage_index]
            surface.blit(image, self.tile.pos)
        else:
            # centre explosion
            surface.blit(Bomb._stage_images[4], self.tile.pos)
            # horizontal arms
            for dx in [1, -1]:
                for step in range(1, self.radius + 1):
                    nx = self.grid_pos[0] + dx * step
                    if not (0 <= nx < cfg.GRID_WIDTH):
                        break
                    pos = (self.tile.pos[0] + cfg.TILE_SIZE * dx * step, self.tile.pos[1])
                    if Bomb._explosion_horizontal:
                        surface.blit(Bomb._explosion_horizontal, pos)
            # vertical arms
            for dy in [1, -1]:
                for step in range(1, self.radius + 1):
                    ny = self.grid_pos[1] + dy * step
                    if not (0 <= ny < cfg.GRID_HEIGHT):
                        break
                    pos = (self.tile.pos[0], self.tile.pos[1] + cfg.TILE_SIZE * dy * step)
                    if Bomb._explosion_vertical:
                        surface.blit(Bomb._explosion_vertical, pos)

    def _explode(self, game_grid: List[tile_module.Tile], players: List[player_module.Player]) -> None:
        """
        Trigger the explosion: mark affected tiles, remove obstacles, and kill players.
        """
        self.exploded = True
        # include the bomb's own tile
        self.explosion_tiles.append(self.tile)
        self.tile.exploding = True
        # propagate outward
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            for step in range(1, self.radius + 1):
                nx = self.grid_pos[0] + dx * step
                ny = self.grid_pos[1] + dy * step
                if not (0 <= nx < cfg.GRID_WIDTH and 0 <= ny < cfg.GRID_HEIGHT):
                    break
                idx = ny * cfg.GRID_WIDTH + nx
                neighbour_tile = game_grid[idx]
                self.explosion_tiles.append(neighbour_tile)
                neighbour_tile.exploding = True
                if neighbour_tile.obstacle:
                    neighbour_tile.obstacle = False
                    neighbour_tile.sprite = tile_module.Tile.empty_tile_sprite
                    break
        # kill players caught in the blast
        for p in players:
            if getattr(p, "state", None) == "dead":
                continue
            for t in self.explosion_tiles:
                if p.grid_pos == t.grid_pos:
                    try:
                        from game.objects.player import states as player_states
                        p.state = "dead"
                        p.update_sprite()    
                    except Exception:
                        pass
                    break
