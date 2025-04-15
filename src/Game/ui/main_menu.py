import pygame
import sys
from Game.assets import config as cfg
from Game.assets import graphics
from Game.systems import input
from Game.ui import button

center_x = cfg.DISPLAY.get_width() // 2
center_y = cfg.DISPLAY.get_height() // 2

images = graphics.images

play_button_image = graphics.resize_image(images["play_button"],0.2)
quit_button_image = graphics.resize_image(images["quit_button"],0.2)





def run():
    running = True # If running is false, it ends the loop, and the run() function returns False, 
                   # to say to launch.py that it should progress to the game loop
    

    def start_game():
        nonlocal running
        running = False

    def quit_game():
        pygame.quit() # If the run() returns True, it tells launch.py that it should quit the game

    
    buttons = [button.Button(play_button_image,(center_x, center_y), start_game),
           button.Button(quit_button_image,(center_x, center_y+300), quit_game)]


    while running:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate

        if input.check_for_quit(): # Check for quitting the game entirely
            return True


        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)
        
        for btn in buttons:       
            btn.draw(cfg.DISPLAY) # Draw buttons
            btn.is_hovered()  # Check if button is hovered for color changing purposes
            if btn.is_clicked():
                btn.perform_action() # Perform the function that the button is given when clicked
            
        
        pygame.display.flip() # Flip the display (Render everything)


    return False