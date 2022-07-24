import csv
import pygame
import os
from pygame import Surface
from typing import Tuple, List

from Game.common import BG, DIRECTORY_ASSETS, SCREEN_HEIGHT, sky_img, mountain_img, pine1_img, pine2_img


def load_animation(scale: float, char_type: str, animation: str) -> List[Surface]:
    animation_list: List[Surface] = []
    num_of_frames: int = len(os.listdir(DIRECTORY_ASSETS + f"img/{char_type}/{animation}/"))
    for i in range(num_of_frames):
        img = pygame.image.load(DIRECTORY_ASSETS + f"img/{char_type}/{animation}/{i}.png").convert_alpha()
        img = scale_image(img, scale)
        animation_list.append(img)
    return animation_list


def load_level(level: int, data: List[int]):
    world_data = data
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    return world_data



def load_explosion_animation(scale: float) -> List[Surface]:
    explosion_images: List[Surface] = []
    for num in range(1, 6):
        img = pygame.image.load(DIRECTORY_ASSETS + f"img/explosion/exp{num}.png").convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        explosion_images.append(img)
    return explosion_images


def draw_bg(screen: Surface, bg_scroll):
    """Draws the background"""
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(6):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 275))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - mountain_img.get_height() - 145))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - mountain_img.get_height() - 25))


def scale_image(image: Surface, scale: float) -> Surface:
    """Resizes image by a factor of input arg `scale`."""
    new_dimension: Tuple[int, int] = (
        int(image.get_width() * scale),
        int(image.get_height() * scale),
    )
    return pygame.transform.scale(image, new_dimension)
