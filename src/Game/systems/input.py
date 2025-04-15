import pygame

def check_for_quit():
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
    return False