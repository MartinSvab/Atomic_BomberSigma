import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
SCREEN = pygame.display.Info()
SCREEN_WIDTH = SCREEN.current_w
SCREEN_HEIGHT = SCREEN.current_h
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atomic BomberSigma")

# Set up clock
clock = pygame.time.Clock()
