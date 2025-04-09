import pygame
from Misc.init import screen, clock, FPS
from Game.Objects import grid,player
import random


TILE_GRID = grid.create_grid()
sigma = random.randint(0,len(TILE_GRID.tiles))
player1 = player.Create_Player(random.uniform(0,1), TILE_GRID.tiles[sigma].pos)

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
        player1.DisplayPlayer(player1.pos,screen)



        # Flip the display
        pygame.display.flip()