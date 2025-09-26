import pygame
import sys
import game.assets.config
from game.assets.graphics import initialize_images

# One time loading of assets
initialize_images()


import game.ui.main_menu as main_menu
import game.core.game_loop as game_loop


if __name__ == "__main__":
    quit = False
    
    while not quit:
        quit = main_menu.run()
        if not quit:
            quit = game_loop.run()
    
    #maybe like a end cutscene here?
    pygame.quit()
    sys.exit()