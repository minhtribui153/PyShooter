from entities import *
from worlds import *

from tqdm import tqdm
import time

# Game Settings
show_settings_menu = False
show_fps = False

switch_button = SwitchButton(SCREEN_WIDTH - 100, 80, off_img, on_img, 0.1)
back_btn = Button(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT - 120, back_img, 0.7)

test = False
def show_loading_assets():
    files_array = count_every_assets()
    for i in tqdm(range(len(files_array)), 
                desc="[GameManager] Loading assets", 
                ascii=False, ncols=100):
        if (files_array[i].endswith("wav") or files_array[i].endswith("mp3")):
            pygame.mixer.Sound(files_array[i])
        elif (files_array[i].endswith("png")):
            pygame.image.load(files_array[i])
        time.sleep(0.05)

def show_loading_levels():
    max_levels = MAX_LEVELS
    if (max_levels == 0): return print("[GameManager] Loading levels: No Levels Found")
    for i in tqdm(range(MAX_LEVELS), 
                desc="[GameManager] Loading levels", 
                ascii=False, ncols=100):
        time.sleep(0.5)

show_loading_assets()
show_loading_levels()


def show_start_menu(exit_game, show_settings_menu):
    start_game = False
    start_intro = False
    screen.fill(BG)
    # Add buttons
    if start_button.draw(screen):
        print(f'[GameManager] Level {level} activated')
        start_game = True
        start_intro = True
    if exit_button.draw(screen): exit_game()
    if settings_button.draw(screen) and not show_settings_menu: show_settings_menu = True
    return start_game, start_intro, show_settings_menu

def show_settings(show_settings_menu, show_fps):
    screen.fill(BG)
    draw_text("Show Frame Per Second (FPS)", font, WHITE, 25, 80)
    if switch_button.draw(screen): show_fps = not show_fps
    if back_btn.draw(screen): show_settings_menu = False
    return show_settings_menu, show_fps

def show_pause_menu(exit_game, world, world_data, player, health_bar):
    global screen, bg_scroll, start_intro, enemy_group, item_box_group, decoration_group, water_group, exit_group
    pause_game = True
    # Draw Menu
    screen.fill(BG)
    # Add buttons
    if resume_button.draw(screen): pause_game = False
    elif restart_button.draw(screen):
        bg_scroll = 0
        death_fade.fade_counter = 0
        world_data = reset_level()
        world_data = load_level(level, world_data)
        world = World()
        player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
        decoration_group, water_group,
        exit_group)
        print(f'[GameManager] Level {level} reactivated')
        intro_fade.fade_counter = 0
        pause_game = False
        start_intro = True
    elif exit_2_button.draw(screen): exit_game()
    elif settings_button.draw(screen): print("Working")
    return player, health_bar, world, world_data, pause_game