import pygame
import numpy as np
import colorsys


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

def shift_hue(surface, hue_shift):
    surface = surface.convert_alpha()  # Ensure it has per-pixel alpha

    # Get RGB and Alpha arrays
    rgb_array = pygame.surfarray.pixels3d(surface).astype(np.float32) / 255.0
    alpha_array = pygame.surfarray.pixels_alpha(surface)

    # Reshape to flat array for processing
    flat_rgb = rgb_array.reshape(-1, 3)
    hsv = np.array([colorsys.rgb_to_hsv(*pixel) for pixel in flat_rgb])
    hsv[:, 0] = (hsv[:, 0] + hue_shift) % 1.0
    new_rgb = np.array([colorsys.hsv_to_rgb(*pixel) for pixel in hsv])
    new_rgb = (new_rgb.reshape(rgb_array.shape) * 255).astype(np.uint8)

    # Create surface with alpha and blit RGB + Alpha onto it
    new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.surfarray.blit_array(new_surface, new_rgb)
    new_surface.lock()
    pygame.surfarray.pixels_alpha(new_surface)[:, :] = alpha_array
    new_surface.unlock()

    return new_surface


#make a script for loading all images in a loop
INTRO_LOGO_image = pygame.image.load("..\\images\\bomberNLogo.png").convert_alpha()
MENU_QUIT_image = pygame.image.load("..\\images\\quit.png").convert_alpha()
MENU_PLAY_image = pygame.image.load("..\\images\\play.png").convert_alpha()
GAME_TILE_image = pygame.image.load("..\\images\\tile.png").convert_alpha()
GAME_PLAYER_image = pygame.image.load("..\\images\\spajt.png").convert_alpha()
GAME_OBSTACLE_image = pygame.image.load("..\\images\\stone.png").convert_alpha()
GAME_BOMBS_array = [pygame.image.load("..\\images\\bomb_1.png").convert_alpha(),
                    pygame.image.load("..\\images\\bomb_2.png").convert_alpha(),
                    pygame.image.load("..\\images\\bomb_3.png").convert_alpha(),
                    pygame.image.load("..\\images\\bomb_4.png").convert_alpha(),]
GAME_EXPLOSION_array = [pygame.image.load("..\\images\\hexplosion.png").convert_alpha(), 
                        pygame.image.load("..\\images\\vexplosion.png").convert_alpha()]