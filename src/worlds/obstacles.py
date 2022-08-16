import pygame

from common import item_boxes
from pygame.surface import Surface
from common.config import TILE_SIZE


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img: Surface, x: float, y: float):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll):
        if player.alive: self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img: Surface, x: float, y: float):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll):
        if player.alive: self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img: Surface, x: float, y: float):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll):
        if player.alive:  self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type: str, x: float, y: float):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll):
        # Scroll
        if player.alive: self.rect.x += screen_scroll
        # Check if player has picked up box
        if pygame.sprite.collide_rect(self, player):
            # Check what kind of box it was
            if self.item_type == "Health":
                player.health += 40
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Ammo":
                player.ammo += 10
            elif self.item_type == "Grenade":
                player.grenades += 3
            # Delete item box
            self.kill()