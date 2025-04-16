import pygame

_event_list = []

def update_event_queue():
    global _event_list
    _event_list = pygame.event.get()

def check_for_quit():
    for event in _event_list:
        if event.type == pygame.QUIT:
            return True
    return False

def check_for_esc():
    for event in _event_list:
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("ESCAPED")
            return True
    return False