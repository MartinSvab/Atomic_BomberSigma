import Misc.image_loader as images
import pygame
from Game.Objects import grid

class Bomb:
    def __init__(self, origin:grid.Tile, planted_time, delay):
        self.location = origin
        self.planted_At = planted_time
        self.explode_At = planted_time + delay



    def DisplayBomb(self, screen, time):
        activeSprite = None
        percentageRemaining = (time - self.planted_At) / (self.explode_At - self.planted_At)


        if percentageRemaining < 0.3:
            activeSprite = images.GAME_BOMBS_array[0]
        elif percentageRemaining < 0.6:
            activeSprite = images.GAME_BOMBS_array[1]
        elif percentageRemaining < 0.9:
            activeSprite = images.GAME_BOMBS_array[2]
        else:
            activeSprite = images.GAME_BOMBS_array[3]
        
        screen.blit(images.ResizeImage(activeSprite, grid.TILE_SIZE/activeSprite.get_width()), self.location.pos)
        return percentageRemaining
    

    def DisplayExplosions(self, screen, tiles:grid):
        neighbours = []
        explosions = images.GAME_EXPLOSION_array

        for index, neighbour in enumerate(self.location.neighbours):
            if neighbour is not None:
                neighbours.append((neighbour,index))

        for neighbour,side in neighbours:
            screen.blit(images.ResizeImage(explosions[side%2], grid.TILE_SIZE/explosions[side%2].get_width()), tiles.tiles[neighbour].pos)


    def Create_Bomb(origin:grid.Tile, planted_time, delay):
        return Bomb(origin, planted_time, delay)