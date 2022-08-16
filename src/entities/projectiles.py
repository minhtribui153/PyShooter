import pygame

from pygame.sprite import Group
from pygame.surface import Surface
from pygame.rect import Rect
from common import SCREEN_WIDTH, ADMIN, ENEMY_DAMAGE, PLAYER_DAMAGE, bullet_img
from common.utils import load_explosion_animation

class Bullet(pygame.sprite.Sprite):
    speed: float
    image: Surface
    rect: Rect
    direction: int

    def __init__(self, x: float, y: float, direction: int):
        pygame.sprite.Sprite.__init__(self)
        # Bullet Configuration
        self.speed = 15
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, world, player, enemy_group: Group, bullet_group: Group, screen_scroll):
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll

        # Check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                if ADMIN: player.health -= 1
                else: player.health -= ENEMY_DAMAGE
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= PLAYER_DAMAGE
                    self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, scale: float):
        pygame.sprite.Sprite.__init__(self)
        # Explosion Configuration
        self.images = load_explosion_animation(scale)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, screen_scroll):
        # Scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # Update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # If animation is complete, delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]