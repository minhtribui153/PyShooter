from json.encoder import INFINITY
import pygame
import os
from typing import Tuple

# Game Configuration
FPS: int = INFINITY * INFINITY
SCREEN_WIDTH: float = 800
SCREEN_HEIGHT: float = SCREEN_WIDTH * 0.8
GAME_TITLE: str = "PyShooter"
DIRECTORY_MAIN: str = os.getcwd()
DIRECTORY_ASSETS: str = DIRECTORY_MAIN + "/src/assets/"
DIRECTORY_LEVELS: str = DIRECTORY_MAIN + "/levels"
PLAYER_JUMP_VEL: int = 11
HEALTH_DYNAMIC_COOLDOWN: int = 5


# Projectile Configuration
GRENADE_TIMER: int  = 100
BULLET_COOLDOWN: int  = 5

# Projectile Damage Configuration
PLAYER_DAMAGE: int  = 20
ENEMY_DAMAGE: int  = 10

# World Configuration 
GRAVITY: float = 0.75
SCROLL_THRESH: int = 150
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21


# Colors
BG: Tuple[int, int, int] = (144, 201, 120)
RED: Tuple[int, int, int] = (255, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLACK: Tuple[int, int, int] = (0, 0, 0)
PINK: Tuple[int, int, int] = (235, 65, 54)