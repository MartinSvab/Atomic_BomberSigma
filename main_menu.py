import pygame
import random
import sys
from init import screen, clock, FPS
import image_loader as image
import detect_clicks as click
from init import SCREEN

logo = image.ResizeImage(image.INTRO_LOGO_image,0.4)
quit = [image.ResizeImage(image.MENU_QUIT_image, 0.2), (2,1.2)]

# Main game loop
def main():
    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if click.checkForClickInBounds(quit[1][0], quit[1][1], (quit[0].get_width(), quit[0].get_height()), pygame.mouse.get_pos()):
                    running = False

        # Update game state here
     




        screen.fill((35,35,35)) #bg
        screen.blit(logo, 
                    ((screen.get_width()/2)-(logo.get_width()/2),screen.get_height()/10)) #logo
        screen.blit(quit[0],
                    ((screen.get_width()/quit[1][0])-(quit[0].get_width()/2), screen.get_height()/quit[1][1])) #quit

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()