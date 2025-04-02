import pygame
import init


def ResizeImage(image, aspect_ratio):
    original = image
    screen_info = pygame.display.Info()

    new_width = int(screen_info.current_w * aspect_ratio)
    new_height = int(screen_info.current_h * aspect_ratio)

    scaled = pygame.transform.smoothscale(original, (new_width, new_height))
    return scaled



INTRO_LOGO_image = pygame.image.load("images\\bomberNLogo.png")

