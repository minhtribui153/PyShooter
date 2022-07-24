import pygame
import enum
from pygame import Surface
from typing import Tuple

"""Game Configuration"""
FPS: int = 100
SCREEN_WIDTH: float = 800
SCREEN_HEIGHT: float = SCREEN_WIDTH * 0.8
GAME_TITLE: str = "Person Shooter"
DIRECTORY_ASSETS: str = "src/Game/assets/"
PLAYER_DAMAGE = 25
ENEMY_DAMAGE = 10

"""World Configuration"""
GRAVITY: float = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 2

"""Colors"""
BG: Tuple[int, int, int] = (144, 201, 120)
RED: Tuple[int, int, int] = (255, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLACK: Tuple[int, int, int] = (0, 0, 0)
PINK: Tuple[int, int, int] = (235, 65, 54)

"""World Sprites"""
# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(DIRECTORY_ASSETS + f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

"""Image Sprites"""
# Button Images
start_img = pygame.image.load(DIRECTORY_ASSETS + "img/start_btn.png")
exit_img = pygame.image.load(DIRECTORY_ASSETS + "img/exit_btn.png")
restart_img = pygame.image.load(DIRECTORY_ASSETS + "img/restart_btn.png")
# Background
pine1_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/pine1.png")
pine2_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/pine2.png")
mountain_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/mountain.png")
sky_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/sky_cloud.png")
# Bullet
bullet_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/bullet.png")
# Grenade
grenade_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/grenade.png")
# Pick Up Boxes
health_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/health_box.png")
ammo_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/ammo_box.png")
grenade_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/grenade_box.png")
item_boxes = {
    "Health": health_box_img,
    "Ammo": ammo_box_img,
    "Grenade": grenade_box_img
}


class ActionType(enum.Enum):
    IDLE = 0
    RUN = 1
    JUMP = 2
    DEATH = 3
