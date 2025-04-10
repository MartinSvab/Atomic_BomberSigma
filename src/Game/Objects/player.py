import Misc.image_loader as images
import pygame
from Game.Objects import grid

class Player:
    def __init__(self, hue, tile):
        self.sprite = images.shift_hue(images.GAME_PLAYER_image, hue)
        self.sprite = images.ResizeImage(self.sprite, grid.TILE_SIZE/self.sprite.get_width())
        self.hue = hue
        self.pos = list(tile.pos)
        self.target_pos = self.pos.copy()
        self.speed = 10  # pixels per frame (you can tweak this)

        
        #add other shit for like bombs and classes

    def DisplayPlayer(self, screen):
        for i in [0, 1]:  # x and y
            if self.pos[i] < self.target_pos[i]:
                self.pos[i] += min(self.speed, self.target_pos[i] - self.pos[i])
            elif self.pos[i] > self.target_pos[i]:
                self.pos[i] -= min(self.speed, self.pos[i] - self.target_pos[i])

        screen.blit(self.sprite, self.pos)

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
            self.target_pos = list(next_tile.pos)
            return next_tile     
        return None
    
    def is_moving(self):
        return self.pos != self.target_pos

    

def Create_Player(hue, pos):
    return Player(hue, pos)