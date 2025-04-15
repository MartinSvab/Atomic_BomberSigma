import Misc.image_loader as images
import pygame
from Game.Objects import grid

class Player:
    def __init__(self, hue, tile):
        self.sprite = images.shift_hue(images.GAME_PLAYER_image, hue)
        self.sprite = images.ResizeImage(self.sprite, grid.TILE_SIZE/self.sprite.get_width())
        self.hue = hue
        self.tile = tile
        self.target_tile = self.tile
        self.speed = 10  # pixels per frame (you can tweak this)

        
        #add other shit for like bombs and classes

    def DisplayPlayer(self, screen):
        for i in [0, 1]:  # x and y
            if self.tile.pos.pos[i] < self.target_tile.pos[i]:
                self.tile.pos[i] += min(self.speed, self.target_tile.pos[i] - self.tile.pos[i])
            elif self.tile.pos[i] > self.target_tile.pos[i]:
                self.tile.pos[i] -= min(self.speed, self.tile.pos[i] - self.target_tile.pos[i])

        screen.blit(self.sprite, self.tile.pos)

    def MovePlayer(self, direction, grid, playerTile):
        next_idx = None
        match direction:
            case "up":
                next_idx=playerTile.neighbours[3]
            case "left":
                next_idx=playerTile.neighbours[2]
            case "right":
                next_idx=playerTile.neighbours[0]
            case "down":
                next_idx=playerTile.neighbours[1]

        if next_idx is not None and grid.tiles[next_idx].obstacle is not True:
            next_tile = grid.tiles[next_idx]
            self.target_tile.pos = list(next_tile.pos)
            return next_tile     
        return None
    
    def is_moving(self):
        return self.tile.pos != self.target_tile.pos

    

def Create_Player(hue, pos):
    return Player(hue, pos)