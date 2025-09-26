import pygame

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h
FPS = 60
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
DISPLAY_CENTER_X = DISPLAY.get_width() // 2
DISPLAY_CENTER_Y = DISPLAY.get_height() // 2
pygame.display.set_caption("Atomic BomberSigma")


# Set up clock
CLOCK = pygame.time.Clock()


# Grid Settings
TILE_SIZE = 128 #defined in pixels
GRID_WIDTH = 8 #defined in tiles    
GRID_HEIGHT = 8 #defined in tiles
BOARD_WIDTH = TILE_SIZE * GRID_WIDTH #defined in pixels
BOARD_HEIGHT = TILE_SIZE * GRID_HEIGHT #defined in pixels
GRID_X_POS = (SCREEN_WIDTH - BOARD_WIDTH) / 2 #pixels!
GRID_Y_POS = (SCREEN_HEIGHT - BOARD_HEIGHT) / 2 #YAYY PIXELS
PLAYER_HUD_SIZE = (400,200)
PLAYER_HUD_MARGIN = 20


# Local settings
LOCAL_PLAYERS = 1
DEFAULT_BOMB_COOLDOWN = 3000 #In ms


#Miscellanesus
TILE_OBSTACLE_CHANCE = 0.2
POWER_UP_DROP_CHANCE = 1      # % on destroyed obstacle
SPEED_BOOST_MULTIPLIER = 1.5     # % faster
SPEED_BOOST_DURATION_MS = 5000   # 5 seconds
