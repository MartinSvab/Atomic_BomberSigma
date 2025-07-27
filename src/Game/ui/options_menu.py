import pygame
from game.assets.keybinds import keybinds
import game.assets.config as cfg
from game.assets import graphics
from game.systems import input 
from game.ui import button

font = pygame.font.SysFont(None, 24)


def run():
    in_menu = True # Tells us whether player is in menu or not (used for exiting out of it)
    should_quit = False # Gets returned, if true, exits the game from the main menu, if not, proceeds to menu normally

    images = graphics.images
    return_button_image = graphics.resize_image(images["return_button"],1)
    player_count = cfg.LOCAL_PLAYERS

    def return_to_main_menu():
        nonlocal in_menu
        in_menu = False

    def quit_game():
        nonlocal in_menu
        in_menu = False 
        nonlocal should_quit
        should_quit = True

    def increase_player_count():
        nonlocal player_count
        if player_count < 4 and player_count > 0:
            player_count += 1
    
    def decrease_player_count():
        nonlocal player_count
        if player_count < 5 and player_count > 1:
            player_count -= 1


    _keybinding_pos = ((cfg.PLAYER_HUD_MARGIN), (cfg.DISPLAY.get_height()*0.5))
    _keybinding_area = (((cfg.DISPLAY.get_width()/2)-(cfg.PLAYER_HUD_MARGIN*2)),(cfg.DISPLAY.get_height()*0.5 - cfg.PLAYER_HUD_MARGIN))


    buttons = [
        button.Button(return_button_image, (0 + return_button_image.get_width()/2, 0 + return_button_image.get_height()/2), return_to_main_menu),
        button.Button(images["plus_button"], (1000,640),increase_player_count,None),
        button.Button(images["minus_button"], (1100, 640), decrease_player_count, None)
               ]

    while in_menu:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates event queue

        if input.check_for_quit(): # Check for quitting the game entirely
           quit_game()

        if input.check_for_esc():
            return_to_main_menu()

        player_count_text = font.render(str(player_count),True,"red")

        #================RENDERING================
                   
        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)

        #All buttons get rendered
        for btn in buttons:
            btn.draw(cfg.DISPLAY) # Draw buttons
            if btn.is_clicked():
                btn.perform_action()
        
        
        cfg.DISPLAY.blit(player_count_text, (650,750))

        #Draws keybinds, according to number of players.
        pygame.draw.rect(cfg.DISPLAY, "black", (_keybinding_pos, _keybinding_area))
        
        for i in range(player_count):
            if (i % 2): #Left side
                if (i < 1): #Up
                    keybinds_center_point = (_keybinding_pos + _keybinding_area[0]/0.25, _keybinding_pos + _keybinding_area[1]/0.25)



        pygame.display.flip() # Flip the display (Render everything)


    cfg.LOCAL_PLAYERS = player_count
    return should_quit