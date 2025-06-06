import pygame
from game.assets import config as cfg
from game.assets import graphics
from game.systems import input
from game.ui import button, options_menu



def run():
    running = True # If running is false, it ends the loop, and the run() function returns should_quit, 
    should_quit = False # to say to launch.py whether it should progress to the game loop or exit
    
    images = graphics.images

    play_button_image = graphics.resize_image(images["play_button"],0.2)
    options_button_image = graphics.resize_image(images["options_button"],0.2)
    quit_button_image = graphics.resize_image(images["quit_button"],0.2)
    logo_image = graphics.resize_image(images["logo"],0.8)


    def start_game():
        nonlocal running
        running = False

    def quit_game():
        nonlocal running
        running = False 
        nonlocal should_quit
        should_quit = True

    def open_options():
        quit_from_options = options_menu.run()
        if quit_from_options:
            quit_game()

    
    buttons = [button.Button(play_button_image,(cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y), start_game),
               button.Button(options_button_image,(cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y + 150), open_options),
           button.Button(quit_button_image,(cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y + 300), quit_game),
           button.Button(logo_image,(cfg.DISPLAY_CENTER_X, cfg.DISPLAY_CENTER_Y-300),None)]


    while running:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates event queue

        if input.check_for_quit(): # Check for quitting the game entirely
            quit_game()

        
        #================RENDERING================

        
        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)


        
        
        for btn in buttons:       
            btn.draw(cfg.DISPLAY) # Draw buttons
            if btn.is_clicked():
                btn.perform_action() # Perform the function that the button is given when clicked
            
        
        pygame.display.flip() # Flip the display (Render everything)


    return should_quit