import pygame

from game.assets import config as cfg
from game.assets import graphics
from game.assets.graphics import shift_hue
from game.assets.keybinds import keybinds
from game.ui import button

font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 34)


class HueSlider:
    _shared_track: pygame.Surface | None = None

    def __init__(self, center_pos: tuple[int, int], size: tuple[int, int], initial_value: float):
        self.pos = center_pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.container_rect = pygame.Rect(
            self.slider_left_pos,
            self.slider_top_pos,
            self.size[0],
            self.size[1],
        )

        initial_value = max(0.0, min(1.0, initial_value))
        button_x = self.slider_left_pos + int((self.size[0] - 1) * initial_value)
        self.button_rect = pygame.Rect(button_x - 9, self.slider_top_pos - 6, 18, self.size[1] + 12)

        if HueSlider._shared_track is None or HueSlider._shared_track.get_size() != self.size:
            HueSlider._shared_track = self._build_gradient_surface(self.size)

    @staticmethod
    def _build_gradient_surface(size: tuple[int, int]) -> pygame.Surface:
        width, height = size
        gradient = pygame.Surface(size, pygame.SRCALPHA)
        for x in range(width):
            hue = x / max(1, width - 1)
            color = pygame.Color(0)
            color.hsva = (hue * 360, 100, 100, 100)
            pygame.draw.line(gradient, color, (x, 0), (x, height))
        return gradient

    def move_slider(self, mouse_pos: tuple[int, int]):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def get_value(self) -> float:
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos
        return max(0.0, min(1.0, button_val / max(1, val_range)))

    def draw(self, surface: pygame.Surface):
        border_color = "white" if self.hovered or self.grabbed else "darkgray"
        surface.blit(HueSlider._shared_track, self.container_rect.topleft)
        pygame.draw.rect(surface, border_color, self.container_rect, width=2, border_radius=8)
        pygame.draw.rect(surface, (235, 235, 235), self.button_rect, border_radius=6)
        pygame.draw.rect(surface, "black", self.button_rect, width=2, border_radius=6)


class PlayerCustomizationUI:
    def __init__(self):
        self.images = graphics.images
        self.player_count = cfg.LOCAL_PLAYERS
        self.on_confirm = None
        self.done = False
        self.editing_bind = None

        self.kb_icons = {
            "left": self.images["keybind_left"],
            "up": self.images["keybind_up"],
            "right": self.images["keybind_right"],
            "down": self.images["keybind_down"],
            "bomb": self.images["keybind_bomb"],
        }
        self.directions = ["left", "up", "right", "down", "bomb"]
        self.bind_index_by_direction = {
            "left": 0,
            "down": 1,
            "right": 2,
            "up": 3,
            "bomb": 4,
        }
        self.player_icon_base = self.images["icon_player_sigma"]

        self._ensure_player_data(self.player_count)
        self.buttons: list[button.Button] = []
        self.player_panels: list[dict] = []
        self._rebuild_ui()

    def _ensure_player_data(self, n_players: int):
        default_row = [
            pygame.K_a,
            pygame.K_s,
            pygame.K_d,
            pygame.K_w,
            pygame.K_SPACE,
        ]
        while len(keybinds) < n_players:
            keybinds.append(default_row.copy())

        if not hasattr(cfg, "PLAYER_HUES"):
            cfg.PLAYER_HUES = []

        default_hues = [0.0, 0.33, 0.66, 0.16]
        while len(cfg.PLAYER_HUES) < n_players:
            cfg.PLAYER_HUES.append(default_hues[len(cfg.PLAYER_HUES) % len(default_hues)])

    def _rebuild_ui(self):
        self.player_panels = []
        self.buttons = []

        panel_size = (820, 260)
        origin_x = 130
        origin_y = 120
        gap_x = 40
        gap_y = 34

        for player_index in range(self.player_count):
            row = player_index // 2
            col = player_index % 2
            x = origin_x + col * (panel_size[0] + gap_x)
            y = origin_y + row * (panel_size[1] + gap_y)
            panel_rect = pygame.Rect(x, y, panel_size[0], panel_size[1])
            slider = HueSlider(
                center_pos=(x + 235, y + 185),
                size=(310, 24),
                initial_value=cfg.PLAYER_HUES[player_index],
            )

            bind_buttons = []
            bind_start_x = x + 385
            bind_y = y + 84
            bind_step_x = 74
            for direction_name in self.directions:
                img = self.kb_icons[direction_name]
                pos = (bind_start_x + len(bind_buttons) * bind_step_x, bind_y)

                def make_action(p_idx, dir_name):
                    def action():
                        self.editing_bind = (p_idx, dir_name)
                    return action

                bind_button = button.Button(img, pos, make_action(player_index, direction_name), label=direction_name)
                bind_button.meta = {"player": player_index, "direction": direction_name}
                bind_buttons.append(bind_button)

            self.buttons.extend(bind_buttons)
            self.player_panels.append(
                {
                    "player": player_index,
                    "rect": panel_rect,
                    "slider": slider,
                    "bind_buttons": bind_buttons,
                }
            )

        plus_btn = button.Button(
            self.images["plus_button"],
            (cfg.DISPLAY_CENTER_X + 70, cfg.DISPLAY_CENTER_Y + 430),
            self._increase_player_count,
        )
        minus_btn = button.Button(
            self.images["minus_button"],
            (cfg.DISPLAY_CENTER_X + 170, cfg.DISPLAY_CENTER_Y + 430),
            self._decrease_player_count,
        )
        self.buttons.extend([plus_btn, minus_btn])

    def _increase_player_count(self):
        if self.player_count < 4:
            self.player_count += 1
            self._ensure_player_data(self.player_count)
            self._rebuild_ui()

    def _decrease_player_count(self):
        if self.player_count > 1:
            if self.editing_bind is not None and self.editing_bind[0] == self.player_count - 1:
                self.editing_bind = None
            self.player_count -= 1
            self._rebuild_ui()

    def handle_events(self, events):
        for event in events:
            if self.editing_bind is not None and event.type == pygame.KEYDOWN:
                player_index, direction = self.editing_bind
                if 0 <= player_index < self.player_count:
                    direction_index = self.bind_index_by_direction[direction]
                    keybinds[player_index][direction_index] = event.key
                self.editing_bind = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for panel in self.player_panels:
                    slider = panel["slider"]
                    if slider.container_rect.collidepoint(event.pos) or slider.button_rect.collidepoint(event.pos):
                        slider.grabbed = True
                        slider.move_slider(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for panel in self.player_panels:
                    panel["slider"].grabbed = False

            for btn in self.buttons:
                btn.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.on_confirm:
                    self.on_confirm()

        mouse_pos = pygame.mouse.get_pos()
        for panel in self.player_panels:
            slider = panel["slider"]
            if slider.grabbed:
                slider.move_slider(mouse_pos)
            slider.hovered = slider.container_rect.collidepoint(mouse_pos) or slider.button_rect.collidepoint(mouse_pos)
            cfg.PLAYER_HUES[panel["player"]] = slider.get_value()

    def draw(self, surface: pygame.Surface):
        for panel in self.player_panels:
            player_index = panel["player"]
            panel_rect = panel["rect"]
            slider = panel["slider"]

            pygame.draw.rect(surface, "grey", panel_rect, border_radius=12)
            pygame.draw.rect(surface, "white", panel_rect, width=3, border_radius=12)

            header = title_font.render(f"Player {player_index + 1}", True, "white")
            surface.blit(header, (panel_rect.x + 24, panel_rect.y + 18))

            icon = shift_hue(self.player_icon_base, cfg.PLAYER_HUES[player_index])
            icon_rect = icon.get_rect(topleft=(panel_rect.x + 28, panel_rect.y + 62))
            surface.blit(icon, icon_rect)

            slider.draw(surface)

            for bind_button in panel["bind_buttons"]:
                bind_button.draw(surface)

                direction = bind_button.meta["direction"]
                if self.editing_bind is not None and self.editing_bind == (player_index, direction):
                    text_label = "..."
                else:
                    direction_index = self.bind_index_by_direction[direction]
                    text_label = pygame.key.name(keybinds[player_index][direction_index])

                text_surf = font.render(text_label, True, "white")
                text_rect = text_surf.get_rect(center=(bind_button.rect.centerx, bind_button.rect.bottom + 16))
                surface.blit(text_surf, text_rect)

        for btn in self.buttons[-2:]:
            btn.draw(surface)

        cfg.LOCAL_PLAYERS = self.player_count

    def confirm(self):
        self.done = True
