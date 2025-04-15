import pygame
from Misc.init import screen, clock, FPS
from Game.Objects import grid,player,bomb
import random



def run():
    TILE_GRID = grid.Create_Grid()
    playerTile = TILE_GRID.tiles[random.randint(0,64)-1]
    player1 = player.Create_Player(random.uniform(0,1), playerTile)
    MOVEMENT_COOLDOWN = 250
    last_move_time = 0
    ACTIVE_BOMBS = []


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


        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        #movement handling

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
        

        #bomb handling

        if not player1.is_moving() and not playerTile.bomb:
            if keys[pygame.K_SPACE]:
                ACTIVE_BOMBS.append(bomb.Bomb.Create_Bomb(playerTile,pygame.time.get_ticks(), 2000))



        screen.fill((35,35,35))

        TILE_GRID.DisplayGrid(screen)
        player1.DisplayPlayer(screen)

        for bombs in ACTIVE_BOMBS:
            percent = bombs.DisplayBomb(screen, pygame.time.get_ticks())
            if percent > 1.1:
                bombs.location.bomb = False
                ACTIVE_BOMBS.remove(bombs)
            elif percent < 1.1 and percent > 0.9:
                bombs.DisplayExplosions(screen, TILE_GRID)
            

        # Flip the display
        pygame.display.flip()