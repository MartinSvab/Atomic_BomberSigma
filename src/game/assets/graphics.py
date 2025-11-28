import pygame
import numpy as np
import colorsys
import os
import sys

# Dictionary of loaded images
images: dict[str, pygame.Surface] = {}


def _get_images_base_path() -> str:
    """
    Return the directory where the image files live.

    - When running from source:   <project_root>/game/assets/images
    - When running as a PyInstaller EXE:
        <_MEIPASS>/game/assets/images
    """
    # Running from a PyInstaller bundle?
    if hasattr(sys, "_MEIPASS"):
        # In the EXE, we will bundle images into game/assets/images
        return os.path.join(sys._MEIPASS, "game", "assets", "images")
    else:
        # Normal dev run: graphics.py lives in game/assets/
        # so images are in game/assets/images
        return os.path.join(os.path.dirname(__file__), "images")


def initialize_images():
    """
    Load all images from the images directory into the global `images` dict.
    Keys are the lowercase filename without extension.
    """
    base_path = _get_images_base_path()

    if not os.path.isdir(base_path):
        raise FileNotFoundError(f"Image directory not found: {base_path!r}")

    all_images = os.listdir(base_path)

    for image in all_images:
        # Skip non-files just in case
        full_path = os.path.join(base_path, image)
        if not os.path.isfile(full_path):
            continue

        image_name = image.split(".")[0].lower()
        surf = pygame.image.load(full_path).convert_alpha()
        images[image_name] = surf


def resize_image(image: pygame.Surface, aspect_ratio: float) -> pygame.Surface:
    original = image

    new_width = int(original.get_width() * aspect_ratio)
    new_height = int(original.get_height() * aspect_ratio)

    scaled = pygame.transform.smoothscale(original, (new_width, new_height))
    return scaled


def rotate_image(image: pygame.Surface, degrees: float) -> pygame.Surface:
    return pygame.transform.rotate(image, degrees)


def shift_hue(surface: pygame.Surface, hue_shift: float) -> pygame.Surface:
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
