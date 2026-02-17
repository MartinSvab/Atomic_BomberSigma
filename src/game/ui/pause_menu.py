import pygame
from game.assets import config as cfg
from game.assets.graphics import images
from game.ui import button as btn

class Pause_menu:
    def __init__(self, surface):
        self.surface = surface
        self.overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
    def pause(self):
        # block here until ESC or a button finishes the pause
        cont = True          # keep running flag for caller
        waiting = True       # stay inside pause loop until an action fires

        def quit_game():
            nonlocal cont, waiting
            cont = False
            waiting = False

        def resume():
            nonlocal waiting
            waiting = False


        resume_button = btn.Button(
            images["resume_button"],
            (cfg.DISPLAY.get_width() / 2, (cfg.DISPLAY.get_height() - 600) / 2),
            resume,
        )
        quit_button = btn.Button(
            images["menu_button"],
            (cfg.DISPLAY.get_width() / 2, (cfg.DISPLAY.get_height() + 600) / 2),
            quit_game,
        )
        buttons = [resume_button, quit_button]

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

        return cont
