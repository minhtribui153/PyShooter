import platform
import pygame

# Define font
font_size = 40
if platform.system() == "Darwin": font_size = 20
font = pygame.font.SysFont('Futura', font_size)