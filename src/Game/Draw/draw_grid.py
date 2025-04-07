import random
import pygame
from Misc.init import screen


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


#-actual displaying-

def draw_grid():
    for row in range(GRID_WIDTH):
        for col in range(GRID_HEIGHT):
            x = GRID_X_POS + (row*TILE_SIZE)
            y = GRID_Y_POS + (col*TILE_SIZE)

            tile = pygame.Rect(x,y,TILE_SIZE,TILE_SIZE)

            pygame.draw.rect(screen,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),tile)