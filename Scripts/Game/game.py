import pygame
from Scripts.Misc.init import screen, clock, FPS
from Scripts.Game.Draw import draw_grid

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


        draw_grid.draw_grid()

        screen.fill((23,53,222))

        # Flip the display
        pygame.display.flip()