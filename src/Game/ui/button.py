import pygame

class Button:
    def __init__(self, image, pos, action=None):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.action = action

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.is_hovered()

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def perform_action(self):
        if self.action:
            self.action()
