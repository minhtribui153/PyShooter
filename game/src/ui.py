from entities import *
from worlds import *

from tqdm import tqdm
import time

# Game Settings
show_settings_menu = False
show_fps = False
show_enemy_healthbar = False

fps_switch_button = SwitchButton(SCREEN_WIDTH - 100, 80, off_img, on_img, 0.1)
enemy_healthbar_switch_button = SwitchButton(SCREEN_WIDTH - 100, 120, off_img, on_img, 0.1)

back_btn = Button(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT - 120, back_img, 0.7)

test = False


def show_start_menu(exit_game, show_settings_menu):
    start_game = False
    start_intro = False
    screen.fill(BG)
    # Add buttons
    if start_button.draw(screen):
        start_game = True
        start_intro = True
    if exit_button.draw(screen): exit_game()
    if settings_button.draw(screen) and not show_settings_menu: show_settings_menu = True
    return start_game, start_intro, show_settings_menu

def show_settings(show_settings_menu, show_fps, show_enemy_healthbar):
    screen.fill(BG)
    draw_text("Show Frame Per Second (FPS)", font, WHITE, 25, 80)
    draw_text("Show Enemy Healthbar", font, WHITE, 25, 120)
    if fps_switch_button.draw(screen): show_fps = not show_fps
    if enemy_healthbar_switch_button.draw(screen): show_enemy_healthbar = not show_enemy_healthbar
    if back_btn.draw(screen): show_settings_menu = False
    return show_settings_menu, show_fps, show_enemy_healthbar

def show_pause_menu(show_settings_menu, exit_game, world, world_data, player, health_bar, current_level, intro_fade: ScreenFade):
    global screen, bg_scroll, start_intro, enemy_group, item_box_group, decoration_group, water_group, exit_group, screen_scroll
    pause_game = True
    # Draw Menu
    screen.fill(BG)
    # Add buttons
    if resume_button.draw(screen): pause_game = False
    if restart_button.draw(screen):
        bg_scroll = 0
        world_data = reset_level()
        world_data = load_level(current_level, world_data)
        world = World()
        player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
        decoration_group, water_group,
        exit_group)
        intro_fade.fade_counter = 0
        pause_game = False
        start_intro = True
    if exit_2_button.draw(screen): exit_game()
    if settings_button.draw(screen) and not show_settings_menu: show_settings_menu = True
    return show_settings_menu, player, health_bar, world, world_data, pause_game, current_level, intro_fade