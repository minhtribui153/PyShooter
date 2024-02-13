import pygame
import os
from common.config import DIRECTORY_ASSETS, TILE_SIZE, TILE_TYPES, DIRECTORY_LEVELS


MAX_LEVELS = len([name for name in os.listdir(DIRECTORY_LEVELS) if "data.csv" in name])
# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(DIRECTORY_ASSETS + f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)