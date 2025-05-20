import pygame
from game.systems import movement
from game.assets.config import MOVEMENT_KEYS

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
            return True
    return False

def check_for_movement_input():
    for event in _event_list:
        if event in MOVEMENT_KEYS:
            movement.handle_movement(event)