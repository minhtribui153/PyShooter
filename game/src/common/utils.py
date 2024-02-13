import csv
import pygame
import os
import math

from sys import platform
from pygame import Surface
from tabulate import tabulate
from typing import Tuple, List
from progress.bar import Bar

from common.config import BG, DIRECTORY_ASSETS, SCREEN_HEIGHT, DIRECTORY_LEVELS, GREEN
from common.sprites import sky_img, mountain_img, pine1_img, pine2_img

def load_animation(scale: float, char_type: str, animation: str) -> List[Surface]:
    animation_list: List[Surface] = []
    num_of_frames: int = len(os.listdir(DIRECTORY_ASSETS + f"img/{char_type}/{animation}/"))
    for i in range(num_of_frames):
        img = pygame.image.load(DIRECTORY_ASSETS + f"img/{char_type}/{animation}/{i}.png").convert_alpha()
        img = scale_image(img, scale)
        animation_list.append(img)
    return animation_list

def rect_distance(rect1, rect2):
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        return 'bottom left', math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        return 'top left', math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        return 'top right', math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        return 'bottom right', math.hypot(x2-x1b, y2-y1b)
    elif left:
        return 'left', x1 - x2b
    elif right:
        return 'right', x2 - x1b
    elif top:
        return 'top', y1 - y2b
    elif bottom:
        return 'bottom', y2 - y1b
    else:  # rectangles intersect
        return 'intersection', 0.

def show_console_information(level, level_complete, pause_game, player, score_database):
    clear_console()
    print("------------------------------")
    with Bar(f"Health", color="green", fill="▣", empty_fill = '▢', suffix=f"{player.health}", width=20) as bar:
        bar.index = player.health - 1
        bar.next()
    print("------------------------------")

    print("-------  --------  ------  ----------  -------------  -------------")
    print(tabulate(
        [ 
            [level, show_player_alive(player.alive, level_complete, pause_game), player.ammo, player.grenades, player.score, score_database + player.score]
        ],
        headers=["Level", "Status", "Ammo", "Grenades", "Level Score", "Total Score"],
        tablefmt='simple'
    ))
    print("-------  --------  ------  ----------  -------------  -------------")


def load_level(level: int, data: List[int]):
    world_data = data
    with open(f'{DIRECTORY_LEVELS}/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    return world_data

def show_player_alive(alive: bool, complete: bool, paused: bool) -> str:
    if paused: return "PAUSED"
    elif alive: return "ALIVE"
    elif alive and complete: return "COMPLETED"
    else: return "DEAD"

def clear_console():
    if platform == "win32": os.system("cls")
    else: os.system("clear")

def count_every_assets(default_path: str = DIRECTORY_ASSETS) -> List[str]:
    assets_dir_files: List[str] = [];
    # Iterate directory
    for path in os.listdir(default_path):
        # check if current path is a file
        if os.path.isdir(f"{default_path}/{path}"):
            new_list = []
            new_list.extend(assets_dir_files)
            new_list.extend(count_every_assets(f"{default_path}/{path}"))
            assets_dir_files = new_list
            continue
        else: assets_dir_files.append(f"{default_path}/{path}");
    return assets_dir_files


def load_explosion_animation(scale: float) -> List[Surface]:
    explosion_images: List[Surface] = []
    for num in range(1, 6):
        img = pygame.image.load(DIRECTORY_ASSETS + f"img/explosion/exp{num}.png").convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        explosion_images.append(img)
    return explosion_images

def is_key(event, key: int): return event.key == key

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