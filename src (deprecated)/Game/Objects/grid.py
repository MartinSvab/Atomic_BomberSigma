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
            if tile.obstacle == True:
                screen.blit(images.ResizeImage(images.GAME_OBSTACLE_image, TILE_SIZE/images.GAME_OBSTACLE_image.get_width()),(tile.pos))




class Tile:
    def __init__(self, pos:tuple[float,float], sprite, obstacle):
        self.pos = pos
        self.sprite = sprite
        self.obstacle = obstacle
        self.neighbours = []
        self.bomb = False
    
    def AssignNeighbours(self,tiles):
        directions = [
            (128,0), #right 0
            (0,128), #down 1
            (-128,0), #left 2
            (0,-128)] #up 3
        neighboursLen = 0
        for direction in directions:
            for index, tile in enumerate(tiles):
                dx, dy = direction
                target_pos = (self.pos[0] + dx, self.pos[1] + dy)
                if target_pos== tile.pos:
                    self.neighbours.append(index)
            if neighboursLen == len(self.neighbours):
                self.neighbours.append(None)
            neighboursLen += 1






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

def Create_Grid():
    tiles=[]
    for col in range(GRID_HEIGHT):
        for row in range(GRID_WIDTH):
            x = GRID_X_POS + (row*TILE_SIZE)
            y = GRID_Y_POS + (col*TILE_SIZE)

            sprite = pygame.transform.rotate(images.GAME_TILE_image, (random.randint(0,3)*90))
            sprite = images.ResizeImage(sprite,TILE_SIZE/sprite.get_width()).convert_alpha()

            #decide if tile has obstacle
            if random.randint(0, 5) == 2:
                tile = Tile((x,y), sprite, True)
            else:
                tile = Tile((x,y), sprite, False)

            tiles.append(tile)

    for tile in tiles:
        #pass neighbouring tiles to tile
        tile.AssignNeighbours(tiles)
            

    grid = Grid((x,y),tiles)        
    return grid

