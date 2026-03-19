import pygame
from game.assets import config as cfg
from game.assets import graphics
from game.assets.graphics import images
from game.ui import button as btn

class Pause_menu:
    def __init__(self, surface):
        self.surface = surface
        self.overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
    def pause(self):
        # block here until ESC or a button finishes the pause
        action = "resume"
        waiting = True

        def go_to_menu():
            nonlocal action, waiting
            action = "menu"
            waiting = False

        def quit_game():
            nonlocal action, waiting
            action = "quit"
            waiting = False

        def resume():
            nonlocal action, waiting
            action = "resume"
            waiting = False

        def play_again():
            nonlocal action, waiting
            action = "restart"
            waiting = False

        button_scale = 0.5
        center_x = cfg.DISPLAY.get_width() / 2
        center_y = cfg.DISPLAY.get_height() / 2
        vertical_spacing = 220

        resume_button = btn.Button(
            graphics.resize_image(images["resume_button"], button_scale),
            (center_x, center_y - vertical_spacing),
            resume,
        )
        again_button = btn.Button(
            graphics.resize_image(images["again_button"], button_scale),
            (center_x, center_y),
            play_again,
        )
        quit_button = btn.Button(
            graphics.resize_image(images["menu_button"], button_scale),
            (center_x, center_y + vertical_spacing),
            go_to_menu,
        )
        buttons = [resume_button, again_button, quit_button]

        # simple event loop while paused
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    resume()

                for butn in buttons:
                    butn.handle_event(event)

            self.overlay.fill((35, 35, 35, 125))
            self.surface.blit(self.overlay, (0, 0))

            for butn in buttons:
                butn.draw(self.surface)

            pygame.display.flip()
            cfg.CLOCK.tick(cfg.FPS)

        return action
