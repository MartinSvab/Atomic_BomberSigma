import pygame
import sys
import game.core.main_menu as main_menu
import game.core.game_loop as game_loop
import game.core.pregame_phase as mpp


def run():
    quit = False
    restart_match = False
    
    while not quit:
        go_back = False

        if not restart_match:
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
        else:
            quit = False
            restart_match = False

        if not quit and not go_back == True:
            game_result = game_loop.run() #actual game loop
            if game_result == "restart":
                restart_match = True
                quit = False
            else:
                quit = game_result
    
    #maybe like a end cutscene here?
    pygame.quit()
    sys.exit()
