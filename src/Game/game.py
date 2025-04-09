import pygame
from Misc.init import screen, clock, FPS
from Game.Objects import grid,player
import random



def run():
    TILE_GRID = grid.Create_Grid()
    playerTile = TILE_GRID.tiles[random.randint(0,64)]
    player1 = player.Create_Player(random.uniform(0,1), playerTile)

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

                    #movement handling
                    if event.key == pygame.K_w:
                        playerTile = TILE_GRID.tiles[player1.MovePlayer("up", TILE_GRID, playerTile)]
                    if event.key == pygame.K_a:
                        playerTile = TILE_GRID.tiles[player1.MovePlayer("left", TILE_GRID, playerTile)]
                    if event.key == pygame.K_d:
                        playerTile = TILE_GRID.tiles[player1.MovePlayer("right", TILE_GRID, playerTile)]
                    if event.key == pygame.K_s:
                        playerTile = TILE_GRID.tiles[player1.MovePlayer("down", TILE_GRID, playerTile)]




        screen.fill((35,35,35))

        TILE_GRID.DisplayGrid(screen)
        player1.DisplayPlayer(player1.pos,screen)



        # Flip the display
        pygame.display.flip()