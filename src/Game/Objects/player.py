import Misc.image_loader as images
import pygame
from Game.Objects import grid

class Player:
    def __init__(self, hue, pos):
        self.sprite = images.shift_hue(images.GAME_PLAYER_image, hue)
        self.sprite = images.ResizeImage(self.sprite, grid.TILE_SIZE/self.sprite.get_width())
        self.hue = hue
        self.pos = pos
        
        #add other shit for like bombs and classes

    def DisplayPlayer(self, pos, screen):
        screen.blit(self.sprite,  pos)



def Create_Player(hue, pos):
    return Player(hue, pos)