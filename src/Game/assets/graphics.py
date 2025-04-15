import pygame
import numpy as np
import colorsys
import os


#TODO = RESIZE ALL IMAGES WHEN LOADING THEM TO THEIR APPROPRIATE SIZE (TILE SIZE)

images = {}


def initialize_images():
    path_to_images = "../images/"

    all_images = os.listdir(path_to_images)
    
    for image in all_images:
        image_name = image.split(".")[0].lower()
        full_path = os.path.join(path_to_images, image)
        images[image_name] = pygame.image.load(full_path).convert_alpha()

def resize_image(image, aspect_ratio):
    original = image

    new_width = int(original.get_width() * aspect_ratio)
    new_height = int(original.get_height() * aspect_ratio)

    scaled = pygame.transform.smoothscale(original, (new_width, new_height))
    return scaled

def rotate_image(image, degrees):
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
