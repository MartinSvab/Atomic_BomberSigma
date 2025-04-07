import random
import pygame
from Misc import image_loader as images
from Misc.init import screen



class Grid:
    def __init__(self, pos:tuple[float,float], tiles):
        self.pos = pos
        self.tiles = tiles

    def DisplayGrid(self, screen):
        for tile in self.tiles:
            screen.blit(tile.sprite,(tile.pos))




class Tile:
    def __init__(self, pos:tuple[float,float], sprite):
        self.pos = pos
        self.sprite = sprite






#-config-

TILE_SIZE = 128 #defined in pixels
GRID_WIDTH = 8 #defined in tiles
GRID_HEIGHT = 8 #defined in tiles

BOARD_WIDTH = TILE_SIZE * GRID_WIDTH #defined in pixels
BOARD_HEIGHT = TILE_SIZE * GRID_HEIGHT #defined in pixels

WINDOW_WIDTH = screen.get_width() #pixels i think
WINDOW_HEIGHT = screen.get_height() #pixels??

GRID_X_POS = (WINDOW_WIDTH - BOARD_WIDTH) / 2 #pixels!
GRID_Y_POS = (WINDOW_HEIGHT - BOARD_HEIGHT) / 2 #YAYY PIXELS


#-create the grid-

def create_grid():
    tiles=[]
    for row in range(GRID_WIDTH):
        for col in range(GRID_HEIGHT):
            x = GRID_X_POS + (row*TILE_SIZE)
            y = GRID_Y_POS + (col*TILE_SIZE)

            sprite = pygame.transform.rotate(images.GAME_TILE_image, (random.randint(0,3)*90))
            sprite = images.ResizeImage(sprite,TILE_SIZE/sprite.get_width()).convert_alpha()

            tile = Tile((x,y), sprite)
            tiles.append(tile)
            

    grid = Grid((x,y),tiles)        
    return grid

