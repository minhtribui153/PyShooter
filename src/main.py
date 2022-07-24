import csv
import pygame
import platform
from typing import Tuple, List
from pygame import Surface
from pygame.time import Clock
from pygame.sprite import Group
from pygame.font import Font

from Game.common import DIRECTORY_ASSETS, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, WHITE, COLS, ROWS, BG, BLACK, PINK, MAX_LEVELS, bullet_img, grenade_img, \
    start_img, exit_img, restart_img, ActionType
from Game.entities import Grenade, World, ScreenFade
from Game.utils import draw_bg, load_level
from Game.button import Button

# Level Variables
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

# Player Action Variables
moving_left: bool = False
moving_right: bool = False
shoot: bool = False
grenade: bool = False
grenade_thrown: bool = False

pygame.init()

clock: Clock = Clock()
screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Load music and sounds
pygame.mixer.music.load(DIRECTORY_ASSETS + 'audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/jump.wav')
shot_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/shot.wav')
grenade_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/grenade.wav')
jump_fx.set_volume(0.5)
shot_fx.set_volume(0.5)
grenade_fx.set_volume(0.5)


# Define font
font_size = 40
if platform.system() == "Darwin": font_size = 20
font = pygame.font.SysFont('Futura', font_size)


def draw_text(text, font_to_render: Font, text_col: Tuple[int, int, int], x, y):
    img = font_to_render.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_level() -> List:
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data


# Buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# Groups
enemy_group: Group = Group()
bullet_group: Group = Group()
grenade_group: Group = Group()
explosion_group: Group = Group()
item_box_group: Group = Group()
decoration_group: Group = Group()
water_group: Group = Group()
exit_group: Group = Group()

# Screen Fade
death_fade = ScreenFade(2, PINK, 4)
intro_fade = ScreenFade(1, BLACK, 4)

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Load in level data and create world
world_data = load_level(level, world_data)

world = World()
player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group, decoration_group, water_group,
                                        exit_group)
running: bool = True
while running:
    clock.tick(FPS)

    if not start_game:
        # Draw Menu
        screen.fill(BG)
        # Add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            running = False
    else:
        # Update Background
        draw_bg(screen, bg_scroll)
        # Draw world map
        world.draw(player, screen, screen_scroll)
        # Show Player Health
        health_bar.draw(screen, player.health)
        # Show Ammo
        draw_text("AMMO:", font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        # Show grenades
        draw_text(f'GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        player.update(screen)
        player.draw()

        for enemy in enemy_group:
            enemy.ai(world, player, bullet_group, screen_scroll, bg_scroll, water_group, exit_group, shot_fx)
            enemy.update(screen)
            enemy.draw()

        """Update and Draw Groups"""
        # Update
        bullet_group.update(world, player, enemy_group, bullet_group, screen_scroll)
        grenade_group.update(world, player, enemy_group, explosion_group, screen_scroll, grenade_fx)
        explosion_group.update(screen_scroll)
        item_box_group.update(player, screen_scroll)
        decoration_group.update(player, screen_scroll)
        water_group.update(player, screen_scroll)
        exit_group.update(player, screen_scroll)

        # Draw
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # Show intro
        if start_intro:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        """Update player actions"""
        if player.alive:
            # Shoot bullets
            if shoot:
                player.shoot(bullet_group, shot_fx)
            # Throw grenades
            elif grenade and not grenade_thrown and player.grenades > 0:
                grenade = Grenade(
                    player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                    player.rect.top, player.direction
                )
                grenade_group.add(grenade)
                # Reduce Grenades
                player.grenades -= 1
                grenade_thrown = True
            # Jump
            if player.in_air:
                player.update_action(ActionType.JUMP)
            # Move
            elif moving_left or moving_right:
                player.update_action(ActionType.RUN)
            # Idle
            else:
                player.update_action(ActionType.IDLE)
            screen_scroll, level_complete = player.move(world, moving_left, moving_right, bg_scroll, water_group, exit_group)
            bg_scroll -= screen_scroll
            # Check if player completed level
            if level_complete:
                start_intro = True
                level += 1
                if level <= MAX_LEVELS:
                    world_data = reset_level()
                    world_data = load_level(level, world_data)
                    world = World()
                    player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
                                                            decoration_group, water_group,
                                                            exit_group)

        else:
            screen_scroll = 0
            if death_fade.fade(screen):
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    bg_scroll = 0
                    world_data = reset_level()
                    world_data = load_level(level, world_data)
                    world = World()
                    player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
                                                            decoration_group, water_group,
                                                            exit_group)
                    start_intro = True

    for event in pygame.event.get():
        """Quits the game"""
        if event.type == pygame.QUIT:
            running = False

        """Keyboard Controls"""
        # Presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                running = False
        # Releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jump = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()
