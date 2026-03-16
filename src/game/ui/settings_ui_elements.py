import pygame


class Slider: #slider class for volume and other settings
    def __init__(
        self,
        pos: tuple,
        size: tuple,
        initial_val: float,
        min_value: int,
        max_value: int,
        label: str = "",
    ):
        self.pos = pos
        self.size = size
        self.label = label
        self.hovered = False
        self.grabbed = False
        self.font = pygame.font.SysFont(None, 36)

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min_value = min_value
        self.max_value = max_value
        self.initial_val = max(0.0, min(1.0, initial_val))

        self.container_rect = pygame.Rect(
            self.slider_left_pos,
            self.slider_top_pos,
            self.size[0],
            self.size[1],
        )
        button_x = self.slider_left_pos + int((self.size[0] - 1) * self.initial_val)
        self.button_rect = pygame.Rect(button_x - 8, self.slider_top_pos - 6, 16, self.size[1] + 12)

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def draw(self, display):
        border_color = "white" if self.hovered or self.grabbed else "darkgray"
        pygame.draw.rect(display, (90, 90, 90), self.container_rect, border_radius=8)
        pygame.draw.rect(display, border_color, self.container_rect, width=2, border_radius=8)
        pygame.draw.rect(display, (70, 140, 255), self.button_rect, border_radius=6)
        pygame.draw.rect(display, "white", self.button_rect, width=2, border_radius=6)

        label_surface = self.font.render(
            f"{self.label}: {int(round(self.get_value()))}",
            True,
            "white",
        )
        label_rect = label_surface.get_rect(midbottom=(self.pos[0], self.container_rect.top - 12))
        display.blit(label_surface, label_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max_value - self.min_value) + self.min_value

    def set_value(self, value):
        if self.max_value == self.min_value:
            self.button_rect.centerx = self.slider_left_pos
            return

        clamped = max(self.min_value, min(self.max_value, value))
        ratio = (clamped - self.min_value) / (self.max_value - self.min_value)
        self.button_rect.centerx = self.slider_left_pos + int((self.size[0] - 1) * ratio)

    