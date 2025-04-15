import pygame
import sys
from Misc.init import screen, clock, FPS
from Game.game import run as start_game
import Misc.image_loader as image
import Misc.detect_clicks as click


#define images
logo = [image.ResizeImage(image.INTRO_LOGO_image,0.4), (2,10)]
quit = [image.ResizeImage(image.MENU_QUIT_image, 0.2), (2,1.2)]
play = [image.ResizeImage(image.MENU_PLAY_image, 0.2), (2, 2)]

#main game loop
def main():
    running = True
    while running:
        clock.tick(FPS)

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if click.checkForClickInBounds(quit[1][0], quit[1][1], (quit[0].get_width(), quit[0].get_height()), pygame.mouse.get_pos()):
                    running = False
                if click.checkForClickInBounds(play[1][0], play[1][1], (play[0].get_width(), play[0].get_height()), pygame.mouse.get_pos()):
                    start_game()

     




        screen.fill((35,35,35)) #bg
        image.DisplayImage(logo, screen) #logo
        image.DisplayImage(quit, screen) #quit
        image.DisplayImage(play, screen) #play

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()