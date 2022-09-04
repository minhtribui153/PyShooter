import pygame
from common.config import DIRECTORY_ASSETS

# Button Images
start_img = pygame.image.load(DIRECTORY_ASSETS + "img/start_btn.png")
exit_img = pygame.image.load(DIRECTORY_ASSETS + "img/exit_btn.png")
restart_img = pygame.image.load(DIRECTORY_ASSETS + "img/restart_btn.png")
resume_img = pygame.image.load(DIRECTORY_ASSETS + "img/resume_btn.png")
settings_img = pygame.image.load(DIRECTORY_ASSETS + "img/settings_btn.png")
off_img = pygame.image.load(DIRECTORY_ASSETS + "img/switch_false.png")
on_img = pygame.image.load(DIRECTORY_ASSETS + "img/switch_true.png")
# Background
pine1_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/pine1.png")
pine2_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/pine2.png")
mountain_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/mountain.png")
sky_img = pygame.image.load(DIRECTORY_ASSETS + "img/Background/sky_cloud.png")
# Bullet
bullet_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/bullet.png")
bullet_display_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/bullet_2.png")
# Animation
enemy_dead = pygame.image.load(DIRECTORY_ASSETS + "img/enemy/Idle/0.png")
muzzle_flash_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/muzzle_flash.png")
# Grenade
grenade_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/grenade.png")
# Pick Up Boxes
health_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/health_box.png")
ammo_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/ammo_box.png")
grenade_box_img = pygame.image.load(DIRECTORY_ASSETS + "img/icons/grenade_box.png")
item_boxes = { "Health": health_box_img, "Ammo": ammo_box_img, "Grenade": grenade_box_img }