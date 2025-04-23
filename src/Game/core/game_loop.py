import pygame
from game.assets import config as cfg
from game.assets.graphics import images
from game.systems import input
from game.objects import grid,tile

def run():
    running = True
    should_quit = False

    def go_back_to_menu():
        nonlocal running
        running = False

    def quit_game():
        nonlocal running
        running = False 
        nonlocal should_quit
        should_quit = True


    while running:
        cfg.CLOCK.tick(cfg.FPS) # Tick at the desired framerate
        input.update_event_queue() # Updates the event queue

        if input.check_for_quit():
            quit_game()

        if input.check_for_esc():
            go_back_to_menu()

        


        cfg.DISPLAY.fill((35,35,35)) # Fill the display with a color (grey)

        game_grid = grid.create_grid()

        grid.draw_grid(game_grid,cfg.DISPLAY)


        pygame.display.flip() # Flip the display (Render everything)
    
    return should_quit