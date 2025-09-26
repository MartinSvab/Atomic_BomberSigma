"""
Powerup handling: spawn on a tile, draw, pickup, and apply timed effects.
"""

import random
import pygame

from game.assets import config as cfg
from game.assets.graphics import images, resize_image
from game.objects import tile as tile_module
from game.objects import player as player_module

# --- module state -----------------------------------------------------------
_active_powerups = set()  # {Powerup}
_effects = {}             # {player: {"orig_speed": float, "speed_boost_until": int}}

# --- data -------------------------------------------------------------------
class Powerup:
    # registry of available types -> sprite
    _powerups = {
        "speed_boost": resize_image(
            images["powerup_speedboost"],
            cfg.TILE_SIZE / images["powerup_speedboost"].get_width()
        ),
    }

    def __init__(self, tile: tile_module.Tile):
        self.kind = random.choice(list(type(self)._powerups.keys()))
        self.sprite = type(self)._powerups[self.kind]
        self.tile = tile  # the tile we sit on

    def draw(self, surface):
        # center the icon on the tile
        surface.blit(self.sprite, self.tile.pos)


# --- spawner / remover ------------------------------------------------------
def create_powerup(tile: tile_module.Tile) -> Powerup | None:
    """Place a powerup on this tile if empty; return it (or None if already present)."""
    if getattr(tile, "powerup", None) is not None:
        return None
    pu = Powerup(tile)
    tile.powerup = pu
    _active_powerups.add(pu)
    return pu

def remove_powerup(tile: tile_module.Tile) -> None:
    pu = getattr(tile, "powerup", None)
    if pu:
        _active_powerups.discard(pu)
        tile.powerup = None


# --- apply & tick -----------------------------------------------------------
def _apply_speed_boost(pu: Powerup, p: player_module.Player):
    now = pygame.time.get_ticks()
    eff = _effects.setdefault(p, {})
    # remember baseline only the first time
    if "orig_speed" not in eff:
        eff["orig_speed"] = p.move_speed
    p.move_speed = eff["orig_speed"] * getattr(cfg, "SPEED_BOOST_MULTIPLIER", 1.5)
    duration = getattr(cfg, "SPEED_BOOST_DURATION_MS", 5000)
    eff["speed_boost_until"] = now + duration

def apply_and_consume(pu: Powerup, p: player_module.Player):
    if pu.kind == "speed_boost":
        _apply_speed_boost(pu, p)
    # consume
    remove_powerup(pu.tile)

def update_effects():
    """Call every frame: expire timed effects and restore stats."""
    if not _effects:
        return
    now = pygame.time.get_ticks()
    expired_players = []
    for p, eff in list(_effects.items()):
        until = eff.get("speed_boost_until")
        if until is not None and now >= until:
            # restore baseline
            p.move_speed = eff.get("orig_speed", p.move_speed)
            eff.pop("speed_boost_until", None)
            eff.pop("orig_speed", None)
        if not eff:
            expired_players.append(p)
    for p in expired_players:
        _effects.pop(p, None)


# --- drawing ----------------------------------------------------------------
def draw_all(surface):
    for pu in _active_powerups:
        pu.draw(surface)
