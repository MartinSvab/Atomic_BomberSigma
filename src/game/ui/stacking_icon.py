import pygame

from game.assets import config
from game.assets.graphics import images


class StackingIcon:
    """Base icon that:
       - shows grayscale when stack == 0
       - shows colored when stack >= 1
       - overlays 'xN' (1..4 capped) when stack > 1
       Also draws a thin underline below the icon.
    """
    def __init__(
        self,
        icon_surface: pygame.Surface,
        image_key: str,
        overlay_scale: float = 0.5,
        prefix: str = "multiplier_x",
        max_sheet: int = 4,
        underline_color: pygame.Color | str = "black",
        underline_thickness: int = 2
    ):
        self.icon = icon_surface
        # use the same grayscale keying convention as DrainingIcon
        self.icon_gs = images.get(f"{image_key}_grayscale", icon_surface)
        self.overlay_scale = overlay_scale
        self.prefix = prefix
        self.max_sheet = max_sheet
        self.underline_color = underline_color
        self.underline_thickness = underline_thickness

    def draw_stack(self, surface: pygame.Surface, pos: tuple[int, int], stack: int):
        # choose which base to draw (grayscale if none, colored if any)
        base = self.icon if stack >= 1 else self.icon_gs
        surface.blit(base, pos)

        # overlay xN only when stack > 1
        if stack > 1:
            shown = min(stack, self.max_sheet)
            key = f"{self.prefix}{shown}"
            mult_icon = images.get(key)
            if mult_icon:
                if self.overlay_scale != 1.0:
                    ow = int(mult_icon.get_width() * self.overlay_scale)
                    oh = int(mult_icon.get_height() * self.overlay_scale)
                    mult_icon = pygame.transform.smoothscale(mult_icon, (ow, oh))
                mult_pos = (
                    pos[0] + self.icon.get_width()  - mult_icon.get_width(),
                    pos[1] + self.icon.get_height() - mult_icon.get_height()
                )
                surface.blit(mult_icon, mult_pos)

        # underline at the bottom edge of the icon
        x1 = pos[0]
        x2 = pos[0] + self.icon.get_width()
        y  = pos[1] + self.icon.get_height()  # along the bottom edge
        pygame.draw.line(surface, self.underline_color, (x1, y), (x2, y), self.underline_thickness)
