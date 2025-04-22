import pygame
import sys
import time
from game.assets import config as cfg
from game.assets import graphics
from game.systems import input
from game.ui import button

center_x = cfg.DISPLAY.get_width() // 2
center_y = cfg.DISPLAY.get_height() // 2






def run():
    start = time.time()

    running = True # If running is false, it ends the loop, and the run() function returns should_quit, 
    should_quit = False # to say to launch.py whether it should progress to the game loop or exit
    
    images = graphics.images

    play_button_image = graphics.resize_image(images["play_button"],0.2)
    quit_button_image = graphics.resize_image(images["quit_button"],0.2)
    logo_image = graphics.resize_image(images["logo"],0.8)

    print(f"[DEBUG] Image resizing took: {time.time() - start:.3f} seconds")


    def start_game():
        nonlocal running
        running = False

    def quit_game():
        nonlocal running
        running = False 
        nonlocal should_quit
        should_quit = True

    
    buttons = [button.Button(play_button_image,(center_x, center_y), start_game),
           button.Button(quit_button_image,(center_x, center_y+300), quit_game),
           button.Button(logo_image,(center_x, center_y-300),None)]

    print(f"[DEBUG] Menu ready after: {time.time() - start:.3f} seconds")

    while running:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates event queue

        if input.check_for_quit(): # Check for quitting the game entirely
            quit_game()

        
        
        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)


        
        
        for btn in buttons:       
            btn.draw(cfg.DISPLAY) # Draw buttons
            if btn.is_clicked():
                btn.perform_action() # Perform the function that the button is given when clicked
            
        
        pygame.display.flip() # Flip the display (Render everything)


    return should_quit