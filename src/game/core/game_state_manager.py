import pygame
import sys
import game.core.main_menu as main_menu
import game.core.game_loop as game_loop
import game.core.pregame_phase as mpp


def run():
    quit = False
    
    while not quit:
        quit = main_menu.run() #in main menu
        if not quit:
            go_back = mpp.run() #map pick phase
            match go_back:
                case True:
                    quit = False
                case False:
                    pass
                case None:
                    quit = True

        if not quit and not go_back == True:
            quit = game_loop.run() #actual game loop
    
    #maybe like a end cutscene here?
    pygame.quit()
    sys.exit()