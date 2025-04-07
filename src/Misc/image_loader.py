import pygame
import Misc.init as init


def ResizeImage(image, aspect_ratio):
    original = image
    screen_info = pygame.display.Info()

    new_width = int(original.get_width() * aspect_ratio)
    new_height = int(original.get_height() * aspect_ratio)

    scaled = pygame.transform.smoothscale(original, (new_width, new_height))
    return scaled

def DisplayImage(image, target):
   target.blit(image[0],
                    ((target.get_width()/image[1][0])-(image[0].get_width()/2), target.get_height()/image[1][1]))

def RotateImage(image, degrees):
    return pygame.transform.rotate(image,degrees)


#make a script for loading all images in a loop
INTRO_LOGO_image = pygame.image.load("..\\images\\bomberNLogo.png")
MENU_QUIT_image = pygame.image.load("..\\images\\quit.png")
MENU_PLAY_image = pygame.image.load("..\\images\\play.png")
GAME_TILE_image = pygame.image.load("..\\images\\tile.png")