import pygame
from pygame.time import Clock
from pygame.surface import Surface
from pygame.font import Font
from button import Button, SwitchButton
from screen_fade import ScreenFade

from common.config import *
from common.sprites import *
from common.utils import *
from level_logics import *

# Load instances
clock: Clock = Clock()
pygame.display.set_caption(GAME_TITLE)
pygame.display.set_icon(enemy_dead)
screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load music and sounds
pygame.mixer.music.load(DIRECTORY_ASSETS + 'audio/music2.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/jump.wav')
shot_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/shot.wav')
grenade_fx = pygame.mixer.Sound(DIRECTORY_ASSETS + 'audio/grenade.wav')
jump_fx.set_volume(0.7)
shot_fx.set_volume(0.7)
grenade_fx.set_volume(0.7)

# Buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
resume_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150, resume_img, 0.45)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
exit_2_button = Button(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, exit_img, 0.65)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)
settings_button = Button(10, 10, settings_img, 0.35)

switch_button = SwitchButton(10, 70, off_img, on_img, 0.1, False)

# Screen Fade
death_fade = ScreenFade(2, PINK, 4, SCREEN_WIDTH, SCREEN_HEIGHT)
complete_fade = ScreenFade(2, BG, 4, SCREEN_WIDTH, SCREEN_HEIGHT)
intro_fade = ScreenFade(1, BLACK, 4, SCREEN_WIDTH, SCREEN_HEIGHT)


# Instance Utils

def draw_text(text, font_to_render: Font, text_col: Tuple[int, int, int], x, y):
    img = font_to_render.render(text, True, text_col)
    screen.blit(img, (x, y))

def update_player(font: Font, player, world, bg_scroll, screen_scroll, health_bar):
    # Update Background
    draw_bg(screen, bg_scroll)
    # Draw world map
    world.draw(player, screen, screen_scroll)
    # Show Player Health
    health_bar.draw(screen, player.health)

    # Show Ammo
    draw_text("AMMO:", font, WHITE, 10, 35)
    screen.blit(bullet_display_img.convert_alpha(), (90, 45))
    draw_text(f"{player.ammo}", font, WHITE, 110, 35)
    # Show grenades
    draw_text(f'GRENADES: ', font, WHITE, 10, 60)
    screen.blit(grenade_img.convert_alpha(), (135, 65))
    draw_text(f"{player.grenades}", font, WHITE, 150, 60)
    # Show score
    screen.blit(enemy_dead.convert_alpha(), (SCREEN_WIDTH / 2 - 50, 10))
    draw_text(f"{player.score}", font, WHITE, SCREEN_WIDTH / 2, 15)

    # Update and Draw player
    player.update(screen, player)
    player.draw()