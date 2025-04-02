import pygame
import random
import sys
from init import screen, clock, FPS
import image_loader as image


logo = image.ResizeImage(image.INTRO_LOGO_image,0.2)

# Main game loop
def main():
    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state here




        # Draw everything
        screen.fill((35,35,35))
        screen.blit(logo, 
                    ((screen.get_width()/2)-(logo.get_width()/2),screen.get_height()/10))

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()