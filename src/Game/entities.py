import pygame
import random
from pygame import Surface, Rect
from pygame.sprite import Group
from typing import Tuple, List

from Game.utils import load_animation, load_explosion_animation
from Game.common import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_DAMAGE, PLAYER_DAMAGE, SCROLL_THRESH, TILE_SIZE, \
    RED, GREEN, BLACK, \
    bullet_img, \
    grenade_img, item_boxes, img_list, \
    ActionType


class Soldier(pygame.sprite.Sprite):
    def __init__(self, screen: Surface, char_type: str, x: float, y: float, scale: float, speed: float, ammo: int,
                 grenades: int = 0):
        pygame.sprite.Sprite.__init__(self)

        # Configuration - World
        self.screen: Surface = screen

        # Configuration - Player
        self.alive: bool = True
        self.char_type: str = char_type
        self.speed: float = speed
        self.ammo: int = ammo
        self.start_ammo: int = ammo
        self.grenades = grenades
        self.shoot_cooldown: float = 0
        self.health: int = 100
        self.max_health: int = self.health
        self.direction: int = 1
        self.jump: bool = False
        self.in_air: bool = True
        self.flip: bool = False

        self.vel_y: float = 0

        # Configuration -  Animations
        self.animation_list: List = []
        self.frame_index: int = 0
        self.action: ActionType = ActionType.IDLE
        self.update_time: int = pygame.time.get_ticks()

        # Configuration - Healthbar
        self.enemy_healthbar = True

        # Configuration - Enemy
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 200, 15)
        self.idling = False
        self.idling_counter = 0

        # Load all animations for the player
        animation_types: List[str] = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # Temporary list of animations
            temp_list = load_animation(scale, self.char_type, animation)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action.value][self.frame_index]
        self.rect: Rect = self.image.get_rect()
        self.rect.center: Tuple[float, float] = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, world, moving_left: bool, moving_right: bool, bg_scroll, water_group: Group, exit_group: Group):
        screen_scroll = 0
        # Reset movement variables
        dx: float = 0
        dy: float = 0

        # Assign movement variables if moving left/right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # Apply Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Check for collision
        for tile in world.obstacle_list:
            # Check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # If AI hit wall, tell AI to turn around
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            # Check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below ground, i.e, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check if above ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Check for collision with exit
        level_complete = False
        if self.char_type == "player" and pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Check if fallen of map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Check if going off edges of screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == 'player' and self.alive:
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self, bullet_group: Group, shot_fx):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 7
            x = self.rect.centerx + (0.75 * self.rect.size[0] * self.direction)
            y = self.rect.centery
            bullet = Bullet(x, y, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def ai(self, world, player, bullet_group: Group, screen_scroll, bg_scroll, water_group, exit_group, shot_fx):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(ActionType.IDLE)
                self.idling = True
                self.idling_counter = 50
            # Check if AI is near player
            if self.vision.colliderect(player.rect):
                self.update_action(ActionType.IDLE)
                # Shoot
                self.shoot(bullet_group, shot_fx)
            elif not self.idling:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(world, ai_moving_left, ai_moving_right, bg_scroll, water_group, exit_group)
                self.update_action(ActionType.RUN)
                self.move_counter += 1

                # Update AI vision as the enemy moves
                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
        # Scroll
        self.rect.x += screen_scroll

    def update(self, screen: Surface):
        # Update checking
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        ratio = self.health / self.max_health
        if self.char_type == "enemy" and self.enemy_healthbar:
            pygame.draw.rect(screen, BLACK, (self.rect.centerx - 52, self.rect.centery - 42, 90, 20))
            pygame.draw.rect(screen, RED, (self.rect.centerx - 50, self.rect.centery - 40, 85, 15))
            pygame.draw.rect(screen, GREEN, (self.rect.centerx - 50, self.rect.centery - 40, 85 * ratio, 15))

    def update_animation(self):
        # Updates Animation
        ANIMATION_COOLDOWN = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action.value][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If animation ran out, reset back to start
        if self.frame_index >= len(self.animation_list[self.action.value]):
            if self.action == ActionType.DEATH:
                self.frame_index = len(self.animation_list[self.action.value]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action: ActionType):
        # Check if new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.enemy_healthbar = False
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(ActionType.DEATH)

    def draw(self):
        image = pygame.transform.flip(self.image, self.flip, False)
        self.screen.blit(image, self.rect)


class HealthBar:
    def __init__(self, x: float, y: float, health: float, max_health: float):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, screen: Surface, health: float):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class World:
    def __init__(self):
        self.level_length = 0
        self.obstacle_list = []

    def process_data(self, screen: Surface, data, enemy_group: Group, item_box_group: Group, decoration_group: Group,
                     water_group: Group, exit_group: Group):
        self.level_length = len(data[0])
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
                        player = Soldier(screen, 'player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
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

    def update(self, player: Soldier, screen_scroll):
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, direction: int):
        pygame.sprite.Sprite.__init__(self)
        # Bullet Configuration
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, world, player: Soldier, enemy_group: Group, bullet_group: Group, screen_scroll):
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
                player.health -= ENEMY_DAMAGE
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= PLAYER_DAMAGE
                    self.kill()


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

    def update(self, world, player: Soldier, enemy_group: Group, explosion_group: Group, screen_scroll, grenade_fx):
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


class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(
                screen, self.colour,
                (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0,
                              SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(
                screen, self.colour,
                (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter,
                              SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour,
                             (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete
