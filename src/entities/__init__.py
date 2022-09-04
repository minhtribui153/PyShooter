import pygame
import random

from entities.projectiles import *
from entities.weapons import *
from pygame import Surface, Rect
from pygame.sprite import Group
from typing import Tuple, List
from common.utils import load_animation
from common import Button, jump_fx, off_img, on_img, collide_water_fx, fall_fx, HEALTH_DYNAMIC_COOLDOWN, GRAVITY, PLAYER_JUMP_VEL, BULLET_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_THRESH, TILE_SIZE, RED, GREEN, BLACK, muzzle_flash_img, ActionType

class SwitchButton():
    off_button: Button
    on_button: Button
    toggled: bool
    pressed: bool

    def __init__(self, x, y, scale):
        self.off_button = Button(x, y, off_img, scale)
        self.on_button = Button(x, y, on_img, scale)
        self.toggled = False
        self.pressed = False
    
    def draw(self, screen: Surface):
        if self.toggled and self.on_button.draw(screen):
            self.toggled = False
            return True
        elif self.off_button.draw(screen):
            self.toggled = True
            return True
        return False
        

class Soldier(pygame.sprite.Sprite):
    def __init__(self, screen: Surface, char_type: str, x: float, y: float, scale: float, speed: float, ammo: int,
                 grenades: int = 0):
        pygame.sprite.Sprite.__init__(self)

        # Configuration - World
        self.screen: Surface = screen

        # Configuration - Player
        self.alive: bool = True
        self.score = 0
        self.char_type: str = char_type
        self.speed: float = speed
        self.ammo: int = ammo
        self.start_ammo: int = ammo
        self.grenades = grenades
        self.shoot_cooldown: float = 0
        self.health: int = 100
        self.current_health: int = 100
        self.max_health: int = self.health
        self.direction: int = 1
        self.jump: bool = False
        self.in_air: bool = True
        self.flip: bool = False
        self.shot = False

        self.vel_y: float = 0

        # Configuration - Animations
        self.animation_list: List = []
        self.frame_index: int = 0
        self.action: ActionType = ActionType.IDLE
        self.update_time: int = pygame.time.get_ticks()

        # Configuration - Healthbar
        self.enemy_healthbar = True

        # Configuration - Enemy
        self.player_already_received_point = False
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 180, 15)
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

        # Configuration - Muzzle Flash
        self.shoot_img_rect = muzzle_flash_img.get_rect()

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
            jump_fx.play()
            self.vel_y = -PLAYER_JUMP_VEL
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
            collide_water_fx.play()

        # Check for collision with exit
        level_complete = False
        if self.char_type == "player" and pygame.sprite.spritecollide(self, exit_group, False): level_complete = True

        # Check if fallen of map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
            fall_fx.play()

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
            self.shot = True
            self.shoot_cooldown = BULLET_COOLDOWN
            x = self.rect.centerx + (0.75 * self.rect.size[0] * self.direction)
            y = self.rect.centery
            bullet = Bullet(x, y, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def ai(self, world, player, bullet_group: Group, screen_scroll, bg_scroll, water_group, exit_group, shot_fx, screen):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(ActionType.IDLE)
                self.idling = True
                self.idling_counter = 50
            # Check if AI is near player
            if self.vision.colliderect(player.rect) and not self.rect.colliderect(player.rect):
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

                if self.move_counter > TILE_SIZE - 1:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
        if self.alive and not player.alive:
            self.update_action(ActionType.IDLE)
        # Scroll
        self.rect.x += screen_scroll

    def update_shoot(self):
        # Update shoot cooldown
        shoot_img = pygame.transform.flip(muzzle_flash_img, self.flip, False)
        coory = 0.05 * self.rect.size[0]
        if self.in_air: coory -= 6
        self.shoot_img_rect.center = ((self.rect.centerx + (0.6 * self.rect.size[0] * self.direction)), self.rect.centery + coory)
        if self.shoot_cooldown == 0: self.shot = False
        if self.shot: self.screen.blit(shoot_img, self.shoot_img_rect)

    def update(self, screen: Surface, player):
        # Update checking
        self.update_direction()
        self.update_animation()
        self.check_alive(player)
        self.update_shoot()

        # Update cooldown
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        # Calculate health ratio
        if (self.health - self.current_health) < 0: self.current_health -= HEALTH_DYNAMIC_COOLDOWN
        elif (self.health - self.current_health) > 0: self.current_health += HEALTH_DYNAMIC_COOLDOWN
        ratio = self.current_health / self.max_health

        if self.char_type == "enemy" and self.enemy_healthbar:
            pygame.draw.rect(screen, BLACK, (self.rect.centerx - 52, self.rect.centery - 42, 90, 20))
            pygame.draw.rect(screen, RED, (self.rect.centerx - 50, self.rect.centery - 40, 85, 15))
            pygame.draw.rect(screen, GREEN, (self.rect.centerx - 50, self.rect.centery - 40, 85 * ratio, 15))
    
    def update_direction(self):
        if (self.direction == 1): self.flip = False
        else: self.flip = True

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

    def check_alive(self, player):
        if self.health <= 0:
            if self.char_type == 'enemy':
                if not self.player_already_received_point:
                    player.score += 1
                    self.player_already_received_point = True
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
        self.current_health = health
        self.max_health = max_health

    def draw(self, screen: Surface, health: float):
        # Update with new health
        self.health = health
        # Calculate health ratio
        if (self.health - self.current_health) < 0: self.current_health -= HEALTH_DYNAMIC_COOLDOWN
        elif (self.health - self.current_health) > 0: self.current_health += HEALTH_DYNAMIC_COOLDOWN
        ratio = self.current_health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

