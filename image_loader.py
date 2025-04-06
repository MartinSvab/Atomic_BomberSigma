import pygame
import init


def ResizeImage(image, aspect_ratio):
    original = image
    screen_info = pygame.display.Info()

    new_width = int(screen_info.current_w * aspect_ratio)
    new_height = int(screen_info.current_h * aspect_ratio)

    scaled = pygame.transform.smoothscale(original, (new_width, new_height))
    return scaled

def DisplayImage(image, target):
   target.blit(image[0],
                    ((target.get_width()/image[1][0])-(image[0].get_width()/2), target.get_height()/image[1][1]))

INTRO_LOGO_image = pygame.image.load("images\\bomberNLogo.png")
MENU_QUIT_image = pygame.image.load("images\\quit.png")
MENU_PLAY_image = pygame.image.load("images\\play.png")
