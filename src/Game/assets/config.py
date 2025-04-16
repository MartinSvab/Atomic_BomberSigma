import pygame

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h
FPS = 60
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atomic BomberSigma")

# Set up clock
CLOCK = pygame.time.Clock()

# Grid Settings
TILE_SIZE = 128
TILE_SIZE = 128 #defined in pixels
GRID_WIDTH = 8 #defined in tiles
GRID_HEIGHT = 8 #defined in tiles
BOARD_WIDTH = TILE_SIZE * GRID_WIDTH #defined in pixels
BOARD_HEIGHT = TILE_SIZE * GRID_HEIGHT #defined in pixels
GRID_X_POS = (SCREEN_WIDTH - BOARD_WIDTH) / 2 #pixels!
GRID_Y_POS = (SCREEN_HEIGHT - BOARD_HEIGHT) / 2 #YAYY PIXELS

