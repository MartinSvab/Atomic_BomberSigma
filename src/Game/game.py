import pygame
from Misc.init import screen, clock, FPS
from Game.Draw import draw_grid

def run():
    PLAYING = True
    while PLAYING:
        clock.tick(FPS)

        #event handling
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    PLAYING = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        PLAYING = False
                        return


        screen.fill((23,53,222))

        draw_grid.draw_grid()

        # Flip the display
        pygame.display.flip()