import pygame

from typing import Tuple
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.rect import Rect

from common import *
from entities import Soldier, HealthBar
from worlds.config import *
from worlds.obstacles import *

class World:
    def __init__(self):
        self.level_length = 0
        self.obstacle_list = []

    def process_data(self, screen: Surface, data, enemy_group: Group, item_box_group: Group, decoration_group: Group,
                     water_group: Group, exit_group: Group):
        self.level_length = len(data[0])
        default_ammo = 20
        default_grenade = 5
        if ADMIN: default_ammo = default_grenade = 10000
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data: Tuple[Surface, Rect] = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:
                        water = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # Create player
                        player = Soldier(screen, 'player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, default_ammo, default_grenade)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                    elif tile == 16:  # Create enemy
                        enemy = Soldier(screen, 'enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 30)
                        enemy_group.add(enemy)
                    elif tile == 17:  # Create Ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # Create Grenade box
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit_sign = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit_sign)
        return player, health_bar

    def draw(self, player: Soldier, screen: Surface, screen_scroll):
        for tile in self.obstacle_list:
            if player.alive: tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])