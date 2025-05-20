import pygame
import game.assets.config as cfg
from game.assets import graphics
from game.systems import input 
from game.ui import button


def run():
    in_menu = True # Tells us whether player is in menu or not (used for exiting out of it)
    should_quit = False # Gets returned, if true, exits the game from the main menu, if not, proceeds to menu normally

    images = graphics.images
    return_button_image = graphics.resize_image(images["return_button"],1)


    def return_to_main_menu():
        nonlocal in_menu
        in_menu = False

    def quit_game():
        nonlocal in_menu
        in_menu = False 
        nonlocal should_quit
        should_quit = True



    buttons = [button.Button(return_button_image, (0 + return_button_image.get_width()/2, 0 + return_button_image.get_height()/2), return_to_main_menu),
               button.Button()]

    while in_menu:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates event queue

        if input.check_for_quit(): # Check for quitting the game entirely
           quit_game()

        if input.check_for_esc():
            return_to_main_menu()


        #================RENDERING================
                   
        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)

        for btn in buttons:
            btn.draw(cfg.DISPLAY) # Draw buttons
            if btn.is_clicked():
                btn.perform_action()
        

        pygame.display.flip() # Flip the display (Render everything)


    return should_quit