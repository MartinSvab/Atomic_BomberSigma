import pygame

from game.assets import config
from game.assets.graphics import images


class DrainingIcon:
    """Draw a surface cropped from top->bottom by fraction_left (0..1)."""
    def __init__(self, icon_surface: pygame.Surface, image_key):
        self.icon = icon_surface
        self.icon_gs = images[f"{image_key}_grayscale"]

    def draw_fraction(self, surface: pygame.Surface, pos: tuple[int, int], fraction_left: float):
        f = max(0.0, min(1.0, float(fraction_left)))
        full_w = self.icon.get_width()
        full_h = self.icon.get_height()
        vis_h = int(full_h * f)
        # keep bottom visible, cut from top
        src = pygame.Rect(0, full_h - vis_h, full_w, vis_h)
        dest = (pos[0], pos[1] + (full_h - vis_h))
        surface.blit(self.icon_gs, pos)
        if f <= 0:
            return
        surface.blit(self.icon, dest, src)
