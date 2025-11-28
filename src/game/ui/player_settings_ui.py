# game/ui/player_settings_panel.py
import pygame
from game.assets.keybinds import keybinds
from game.assets import config as cfg
from game.assets import graphics
from game.ui import button

font = pygame.font.SysFont(None, 24)

class PlayerSettingsUI:
    def __init__(self):
        self.images = graphics.images
        self.player_count = cfg.LOCAL_PLAYERS
        self.kb_icons = {
            "left":  self.images["keybind_left"],
            "up":    self.images["keybind_up"],
            "right": self.images["keybind_right"],
            "down":  self.images["keybind_down"],
            "bomb":  self.images["keybind_bomb"]
        }
        self.directions = ["left", "up", "right", "down", "bomb"]
        self.editing_bind = None  # (player_idx, direction)
        self.done = False

        self._ensure_keybinds_length(self.player_count)
        self.buttons = self._build_buttons()

    def _ensure_keybinds_length(self, n_players: int):
        default_row = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]
        while len(keybinds) < n_players:
            keybinds.append(default_row.copy())

    def _build_buttons(self):
        bind_buttons = []

        start_x, start_y = 220, 220
        step_x, step_y   = 150, 120

        for p in range(self.player_count):
            for d_i, d in enumerate(self.directions):
                img = self.kb_icons[d]
                pos = (start_x + d_i * step_x, start_y + p * step_y)

                def make_action(player_index, direction_name):
                    def action():
                        self.editing_bind = (player_index, direction_name)
                    return action

                b = button.Button(img, pos, make_action(p, d), label=d)
                b.meta = {"player": p, "direction": d}
                bind_buttons.append(b)

        plus_btn = button.Button(
            self.images["plus_button"],  (1000, 640),
            self._increase_player_count
        )
        minus_btn = button.Button(
            self.images["minus_button"], (1100, 640),
            self._decrease_player_count
        )

        return bind_buttons + [plus_btn, minus_btn]

    def _increase_player_count(self):
        if self.player_count < 4:
            self.player_count += 1
            self._ensure_keybinds_length(self.player_count)
            self.buttons = self._build_buttons()

    def _decrease_player_count(self):
        if self.player_count > 1:
            if self.editing_bind is not None and self.editing_bind[0] == self.player_count - 1:
                self.editing_bind = None
            self.player_count -= 1
            self.buttons = self._build_buttons()

    def handle_events(self, events, on_confirm):
        for event in events:
            if self.editing_bind is not None and event.type == pygame.KEYDOWN:
                p_i, direction = self.editing_bind
                if 0 <= p_i < self.player_count:
                    idx = self.directions.index(direction)
                    keybinds[p_i][idx] = event.key
                self.editing_bind = None

            for btn in self.buttons:
                btn.handle_event(event)

            # You can call on_confirm for example if the player presses Enter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.done = True
                on_confirm()

    def draw(self, surface):
        for btn in self.buttons:
            btn.draw(surface)

            if hasattr(btn, "meta"):
                p = btn.meta["player"]
                d = btn.meta["direction"]
                if self.editing_bind is not None and self.editing_bind == (p, d):
                    text_label = "..."
                else:
                    idx = self.directions.index(d)
                    if p < len(keybinds) and idx < len(keybinds[p]):
                        text_label = pygame.key.name(keybinds[p][idx])
                    else:
                        text_label = ""

                if text_label:
                    text_surf = font.render(text_label, True, "white")
                    surface.blit(
                        text_surf,
                        (btn.rect.centerx - text_surf.get_width() / 2,
                         btn.rect.bottom + 6)
                    )

        cfg.LOCAL_PLAYERS = self.player_count
