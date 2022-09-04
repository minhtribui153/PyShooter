import pygame

from pygame.sprite import Group
from entities.projectiles import Explosion
from common import TILE_SIZE, GRAVITY, grenade_img

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, direction: int):
        pygame.sprite.Sprite.__init__(self)
        # Grenade Configuration
        self.timer = 95
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self, world, player, enemy_group: Group, explosion_group: Group, screen_scroll, grenade_fx):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # Check for collision with level
        for tile in world.obstacle_list:
            # Check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            # Check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # Check if below ground, i.e, thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check if above ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # Update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # Countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # Do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50

            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50