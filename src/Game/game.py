import pygame
from Misc.init import screen, clock, FPS
from Game.Objects import grid,player
import random



def run():
    TILE_GRID = grid.Create_Grid()
    playerTile = TILE_GRID.tiles[random.randint(0,64)]
    player1 = player.Create_Player(random.uniform(0,1), playerTile)
    MOVEMENT_COOLDOWN = 250
    last_move_time = 0


    PLAYING = True
    while PLAYING:
        clock.tick(FPS)

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PLAYING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PLAYING = False
                    return

        #movement handling
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not player1.is_moving() and current_time - last_move_time > MOVEMENT_COOLDOWN:
            direction = None
            if keys[pygame.K_w]:
                direction = "up"
            elif keys[pygame.K_s]:
                direction = "down"
            elif keys[pygame.K_a]:
                direction = "left"
            elif keys[pygame.K_d]:
                direction = "right"

            if direction:
                next_tile = player1.MovePlayer(direction, TILE_GRID, playerTile)
                if next_tile and not next_tile.obstacle:
                    playerTile = next_tile
                    last_move_time = current_time





        screen.fill((35,35,35))

        TILE_GRID.DisplayGrid(screen)
        player1.DisplayPlayer(player1.pos,screen)



        # Flip the display
        pygame.display.flip()