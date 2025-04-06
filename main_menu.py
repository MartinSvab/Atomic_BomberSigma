import pygame
import sys
from init import screen, clock, FPS
import image_loader as image
import detect_clicks as click

logo = [image.ResizeImage(image.INTRO_LOGO_image,0.4), (2,10)]
quit = [image.ResizeImage(image.MENU_QUIT_image, 0.2), (2,1.2)]
play = [image.ResizeImage(image.MENU_PLAY_image, 0.2), (2, 2)]

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
                if click.checkForClickInBounds(play[1][0], play[1][1], (play[0].get_width(), play[0].get_height()), pygame.mouse.get_pos()):
                    print("pressed play")

        # Update game state here
     




        screen.fill((35,35,35)) #bg
        image.DisplayImage(logo, screen) #logo
        image.DisplayImage(quit, screen) #quit
        image.DisplayImage(play, screen) #play

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()