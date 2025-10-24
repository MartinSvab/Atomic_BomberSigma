# game/objects/bomb.py
"""
Bombs for Atomic BomberSigma.

- Place a bomb on a tile; it ticks for `fuse_frames`, then explodes in a cross.
- Explosion removes obstacles, can drop powerups, and kills players on affected tiles.
"""

import pygame
from typing import List, Tuple
import random

from game.assets import config as cfg
from game.assets import graphics
from game.objects import tile as tile_module
from game.objects import player as player_module
from game.objects import powerup as powerup_module


# ---- Tunables ---------------------------------------------------------------

DEFAULT_FUSE_FRAMES = 60              # ~1s at 60 FPS
EXPLOSION_FRAMES = 30                 # how long the explosion graphic lingers
POWERUP_DROP_CHANCE = cfg.POWER_UP_DROP_CHANCE  # 25% in cfg
POWERUP_DROP_TABLE = ["speed_boost", "bomb_range_up", "bomb_cooldown_reduce"]
# ^^ these must match keys from powerup.SPECS


class Bomb:
    """Represents a bomb placed by a player."""

    _stage_images: List[pygame.Surface] = []
    _explosion_horizontal: pygame.Surface | None = None
    _explosion_vertical: pygame.Surface | None = None

    def __init__(
        self,
        tile: tile_module.Tile,
        grid_pos: Tuple[int, int],
        owner: player_module.Player,
        radius: int = 1,
        fuse_frames: int = DEFAULT_FUSE_FRAMES
    ) -> None:
        self.tile = tile
        self.grid_pos = grid_pos
        self.owner = owner

        # radius here is still stored, but we won't rely on it anymore.
        # we will instead ask the owner at explode/draw time.
        self.radius = radius

        self.fuse_frames = fuse_frames
        self._frame_counter = 0

        self.exploded = False
        self.explosion_frames_remaining = EXPLOSION_FRAMES
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
        cls._stage_images.clear()
        for i in range(1, 6):
            key = f"bomb_stage_{i}"
            if key in images:
                ratio = cfg.TILE_SIZE / images[key].get_width()
                cls._stage_images.append(graphics.resize_image(images[key], ratio))

        # Explosion sprites
        if "bomb_explosion_horizontal" in images:
            ratio_h = cfg.TILE_SIZE / images["bomb_explosion_horizontal"].get_width()
            cls._explosion_horizontal = graphics.resize_image(images["bomb_explosion_horizontal"], ratio_h)

        if "bomb_explosion_vertical" in images:
            ratio_v = cfg.TILE_SIZE / images["bomb_explosion_vertical"].get_width()
            cls._explosion_vertical = graphics.resize_image(images["bomb_explosion_vertical"], ratio_v)

    # ----------------------------------- lifecycle ---------------------------

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

        # ask owner for current blast radius for visuals
        blast_radius = max(1, getattr(self.owner, "bomb_range", self.radius))

        if not self.exploded:
            if self.fuse_frames > 0 and Bomb._stage_images:
                # progress 0..len-1 based on fuse time
                stage_index = min(
                    len(Bomb._stage_images) - 1,
                    (self._frame_counter * len(Bomb._stage_images)) // max(1, self.fuse_frames)
                )
                surface.blit(Bomb._stage_images[stage_index], self.tile.pos)
        else:
            #
            # center
            #
            if Bomb._stage_images:
                surface.blit(Bomb._stage_images[-1], self.tile.pos)

            #
            # horizontal arms
            #
            if Bomb._explosion_horizontal:
                for dx in [1, -1]:
                    for step in range(1, blast_radius + 1):
                        nx = self.grid_pos[0] + dx * step
                        if not (0 <= nx < cfg.GRID_WIDTH):
                            break
                        pos = (self.tile.pos[0] + cfg.TILE_SIZE * dx * step,
                               self.tile.pos[1])
                        surface.blit(Bomb._explosion_horizontal, pos)

            #
            # vertical arms
            #
            if Bomb._explosion_vertical:
                for dy in [1, -1]:
                    for step in range(1, blast_radius + 1):
                        ny = self.grid_pos[1] + dy * step
                        if not (0 <= ny < cfg.GRID_HEIGHT):
                            break
                        pos = (self.tile.pos[0],
                               self.tile.pos[1] + cfg.TILE_SIZE * dy * step)
                        surface.blit(Bomb._explosion_vertical, pos)

    # ----------------------------------- internals --------------------------

    def _explode(self, game_grid: List[tile_module.Tile], players: List[player_module.Player]) -> None:
        """
        Trigger the explosion: mark affected tiles, remove obstacles (and maybe drop powerups),
        and kill players on affected tiles.
        """
        self.exploded = True

        # figure out how far this bomb should actually reach when it pops
        blast_radius = max(1, getattr(self.owner, "bomb_range", self.radius))

        # include the bomb's own tile
        self.explosion_tiles.append(self.tile)
        self.tile.exploding = True

        # propagate in 4 directions
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            for step in range(1, blast_radius + 1):
                nx = self.grid_pos[0] + dx * step
                ny = self.grid_pos[1] + dy * step

                # out of bounds? stop this direction
                if not (0 <= nx < cfg.GRID_WIDTH and 0 <= ny < cfg.GRID_HEIGHT):
                    break

                idx = ny * cfg.GRID_WIDTH + nx
                neighbour_tile = game_grid[idx]

                # mark this tile as exploding
                self.explosion_tiles.append(neighbour_tile)
                neighbour_tile.exploding = True

                # if it's an obstacle, break it and maybe drop powerup,
                # but stop the flame from going further past it
                if neighbour_tile.obstacle:
                    neighbour_tile.obstacle = False
                    neighbour_tile.sprite = tile_module.Tile.empty_tile_sprite

                    # optional: drop a random powerup there
                    if getattr(neighbour_tile, "powerup", None) is None:
                        if random.random() < POWERUP_DROP_CHANCE and POWERUP_DROP_TABLE:
                            effect_id = random.choice(POWERUP_DROP_TABLE)
                            try:
                                neighbour_tile.powerup = powerup_module.create_powerup(effect_id)
                            except Exception:
                                # ignore silently if create_powerup fails for that id
                                pass

                    break  # stop going further in this direction

        # kill players caught in the blast
        for p in players:
            if getattr(p, "state", None) == "dead":
                continue
            for t in self.explosion_tiles:
                if p.grid_pos == t.grid_pos:
                    try:
                        p.state = "dead"
                        p.update_sprite()
                    except Exception:
                        pass
                    break
