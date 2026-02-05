# game/ui/map_selection_ui.py
import pygame
from game.assets import config as cfg
from game.systems import map_preview
from game.ui import button
from game.assets import graphics
from game.objects.grid_preset import _presets

class MapSelectionUI:
    def __init__(self):
        self.map_names = list(_presets.keys())
        self.index = 0
        self.done = False

        images = graphics.images
        arrow_left_image  = graphics.resize_image(images["arrow_l"], 0.2)
        arrow_right_image = graphics.resize_image(images["arrow_r"], 0.2)

        self.buttons = [
            button.Button(
                arrow_left_image,
                (cfg.DISPLAY_CENTER_X - 500, cfg.DISPLAY_CENTER_Y),
                self.prev_map
            ),
            button.Button(
                arrow_right_image,
                (cfg.DISPLAY_CENTER_X + 500, cfg.DISPLAY_CENTER_Y),
                self.next_map
            ),
        ]

    @property
    def selected_map_name(self):
        return self.map_names[self.index]

    def prev_map(self):
        self.index = (self.index - 1) % len(self.map_names)

    def next_map(self):
        self.index = (self.index + 1) % len(self.map_names)

    def handle_events(self, events):
        for e in events:
            for b in self.buttons:
                b.handle_event(e)

    def draw(self, surface):
        # let the preview system render the current selection
        scale = 0.5

        rect = map_preview.get_preview_rect(self.selected_map_name, scale)
        pos = (
            cfg.DISPLAY_CENTER_X - rect.w // 2,
            cfg.DISPLAY_CENTER_Y - rect.h // 2
        )

        map_preview.preview_map(self.selected_map_name, pos, cfg.DISPLAY, scale)

        for b in self.buttons:
            b.draw(surface)

    def confirm(self):
        self.done = True
        # if you want to store selection somewhere global, do it here
        # e.g. cfg.SELECTED_MAP = self.selected_map_name
