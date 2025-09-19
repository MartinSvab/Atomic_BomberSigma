import pygame

class Button:
    def __init__(self, image, pos, action=None, label=None):
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)

        self.label = label
        self.action = action

        # click-on-release tracking
        self._pressed_inside = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event):
        """Call this from your main loop for each pygame event."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # start click only if mouse down happened inside the button
            if self.rect.collidepoint(event.pos):
                self._pressed_inside = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # only fire if mouse was pressed on me AND released on me
            if self._pressed_inside and self.rect.collidepoint(event.pos):
                self.perform_action()
            self._pressed_inside = False

    def perform_action(self):
        if self.action:
            self.action()
