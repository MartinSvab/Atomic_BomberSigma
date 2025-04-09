import Misc.image_loader as images
import pygame
from Game.Objects import grid

class Player:
    def __init__(self, hue, tile):
        self.sprite = images.shift_hue(images.GAME_PLAYER_image, hue)
        self.sprite = images.ResizeImage(self.sprite, grid.TILE_SIZE/self.sprite.get_width())
        self.hue = hue
        self.pos = list(tile.pos)
        
        #add other shit for like bombs and classes

    def DisplayPlayer(self, pos, screen):
        screen.blit(self.sprite,  pos)

    def MovePlayer(self, direction, grid, playerTile):
        match direction:
            case "up":
                next_idx=playerTile.neighbours[3]
                if grid.tiles[0].pos[1] < self.pos[1] and next_idx is not None:
                    self.pos[1] -= 128
                    return next_idx
            case "left":
                next_idx=playerTile.neighbours[2]
                if grid.tiles[0].pos[0] < self.pos[0] and next_idx is not None:
                    self.pos[0] -= 128
                    return next_idx
            case "right":
                next_idx=playerTile.neighbours[0]
                if grid.tiles[-1].pos[0] > self.pos[0] and next_idx is not None:
                    self.pos[0] += 128
                    return next_idx
            case "down":
                next_idx=playerTile.neighbours[1]
                if grid.tiles[-1].pos[1] > self.pos[1] and next_idx is not None:
                    self.pos[1] += 128
                    print("DOWN:", self.pos, "last tile y-pos:", grid.tiles[-1].pos[1], "next_idx:", next_idx)

                    return next_idx     
        return None


def Create_Player(hue, pos):
    return Player(hue, pos)