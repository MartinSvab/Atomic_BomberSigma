import pygame
from game.assets import graphics

class Button:
    def __init__(self, image, pos,action=None, label=None):
        self.original_image = image
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=pos)
        self.label = label
        self.action = action
        self.hovered = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.is_hovered()

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def perform_action(self):
        if self.action:
            self.action()