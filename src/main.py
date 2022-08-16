import pygame

from entities import *
from worlds import *
from level_logics import *

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

if MAX_LEVELS > 0:
    # Load in level data and create world
    world_data = load_level(level, world_data)

    world = World()
    player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group, decoration_group, water_group, exit_group)

running: bool = True
if ADMIN: print('[GameManager] WARNING: Blatant mode enabled, game instance can slow down easily')
print('[GameManager] Running...')
while running:
    clock.tick(FPS)
    screen.fill(BLACK)


    if (MAX_LEVELS == 0):
        draw_text("No Levels found", font, WHITE, SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2)
        draw_text("Please build your own level with level_editor.py", font, WHITE, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 30)
    elif not start_game:
        screen.fill(BG)
        # Add buttons
        if start_button.draw(screen):
            print(f'[GameManager] Level {level} activated')
            start_game = True
            start_intro = True
        if exit_button.draw(screen): running = False
    elif pause_game:
        # Draw Menu
        screen.fill(BG)
        # Add buttons
        if resume_button.draw(screen): pause_game = False
        if restart_button.draw(screen):
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
        if exit_2_button.draw(screen): running = False
    else:
        update_player(font, player, world, bg_scroll, screen_scroll, health_bar)

        for enemy in enemy_group:
            enemy.ai(world, player, bullet_group, screen_scroll, bg_scroll, water_group, exit_group, shot_fx, screen)
            enemy.update(screen, player)
            enemy.draw()

        update_pygame_groups(screen, world, player, screen_scroll, grenade_fx)

        # Show intro
        if start_intro:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            # Shoot bullets
            if shoot: player.shoot(bullet_group, shot_fx)
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
            if player.in_air: player.update_action(ActionType.JUMP)
            # Move
            elif moving_left or moving_right: player.update_action(ActionType.RUN)
            # Idle
            else: player.update_action(ActionType.IDLE)
            screen_scroll, level_complete = player.move(world, moving_left, moving_right, bg_scroll, water_group, exit_group)
            bg_scroll -= screen_scroll
            # Check if player completed level
            if level_complete:
                if (print_counter == 0):
                    level += 1
                    print(f"[GameManager] Level {level - 1} complete")
                
                if level <= MAX_LEVELS:
                    score_database += player.score
                    print(f"[GameManager] Total Score: {score_database}")
                    print_counter = 0
                    start_intro = True
                    print(f'[GameManager] Level {level} activated')
                    screen_scroll = 0
                    bg_scroll = 0
                    world_data = reset_level()
                    world_data = load_level(level, world_data)
                    world = World()
                    player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
                                                            decoration_group, water_group,
                                                            exit_group)
                else:
                    if (print_counter == 0):
                        print(f"[GameManager] Game Finished")
                        print(f"[GameManager] Total Score: {score_database}")
                        player.speed = 0
                        print_counter += 1
                    if complete_fade.fade(screen):
                        if restart_button.draw(screen):
                            bg_scroll = 0
                            screen_scroll = 0
                            print_counter = 0
                            level = 1
                            print(f"[GameManager] Game restarted")
                            print(f"[GameManager] Level {level} activated")
                            world_data = reset_level()
                            world_data = load_level(level, world_data)
                            world = World()
                            player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
                                                                    decoration_group, water_group, exit_group)
                            start_intro = True
                    

        else:
            screen_scroll = 0
            if (print_counter == 0):
                print(f'[GameManager] Eliminated on level {level}')
                print_counter += 1
            if death_fade.fade(screen):
                if restart_button.draw(screen):
                    print_counter = 0
                    print(f'[GameManager] Level {level} reactivated')
                    bg_scroll = 0
                    death_fade.fade_counter = 0
                    world_data = reset_level()
                    world_data = load_level(level, world_data)
                    world = World()
                    player, health_bar = world.process_data(screen, world_data, enemy_group, item_box_group,
                                                            decoration_group, water_group,
                                                            exit_group)
                    start_intro = True
    
    draw_text(f"FPS: {round(clock.get_fps())}", font, WHITE, SCREEN_WIDTH - 110, 25)

    for event in pygame.event.get():
        # Quits the game
        if event.type == pygame.QUIT: running = False

        # Keyboard Controls
        # Presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: moving_left = True
            if event.key == pygame.K_d: moving_right = True
            if event.key == pygame.K_SPACE: shoot = True
            if event.key == pygame.K_q: grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                if (player.alive and start_game): pause_game = not pause_game
        # Releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: moving_left = False
            if event.key == pygame.K_d: moving_right = False
            if event.key == pygame.K_SPACE: shoot = False
            if event.key == pygame.K_w or event.key == pygame.K_SPACE: player.jump = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

print('[GameManager] Exit requested, closing all instances...')
pygame.quit()