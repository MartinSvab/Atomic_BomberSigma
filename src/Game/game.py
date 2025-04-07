import pygame
from Misc.init import screen, clock, FPS
from Game.Objects import grid


TILE_GRID = grid.create_grid()

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


        screen.fill((35,35,35))

        
        TILE_GRID.DisplayGrid(screen)

        # Flip the display
        pygame.display.flip()