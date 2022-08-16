from typing import List
from pygame.sprite import Group
from common.config import *

# Groups
enemy_group: Group = Group()
bullet_group: Group = Group()
grenade_group: Group = Group()
explosion_group: Group = Group()
item_box_group: Group = Group()
decoration_group: Group = Group()
water_group: Group = Group()
exit_group: Group = Group()

def update_pygame_groups(screen, world, player, screen_scroll, grenade_fx):
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