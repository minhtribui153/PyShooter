from ui import *

level_complete = False
update_console_cooldown = 0

class GameManager:
    def __init__(self) -> None:
        self.running: bool = True

        # Create empty tile list
        self.world_data = []
        for _ in range(ROWS):
            r = [-1] * COLS
            self.world_data.append(r)
        
        self.player: Soldier = None
        self.health_bar: HealthBar = None
        self.world: World = None
        self.level = 1

        if MAX_LEVELS > 0:
            # Load in level data and create world
            self.world_data = load_level(self.level, self.world_data)

            self.world = World()
            self.player, self.health_bar = self.world.process_data(screen, self.world_data, enemy_group, item_box_group, decoration_group, water_group, exit_group)
    
    def exit_game(self):
        print("[GameManager] Exit requested, closing all instances...")
        self.running = False
    
    def reset_level(self):
        global bg_scroll, death_fade, start_intro
        print("Working")
        bg_scroll = 0
        intro_fade.fade_counter = 0
        death_fade.fade_counter = 0
        self.world_data = reset_level()
        self.world_data = load_level(self.level, self.world_data)
        self.world = World()
        self.player, self.health_bar = self.world.process_data(screen, self.world_data, enemy_group, item_box_group,
                                                decoration_group, water_group,
                                                exit_group)
        start_intro = True

        return 

    def listen_events(self):
        global moving_left, moving_right, shoot, grenade, grenade_thrown, pause_game
        for event in pygame.event.get():
            # Quits the game
            if event.type == pygame.QUIT: self.exit_game()

            # Keyboard Controls
            # Presses
            if event.type == pygame.KEYDOWN:
                if is_key(event, pygame.K_a) or is_key(event, pygame.K_LEFT): moving_left = True
                if is_key(event, pygame.K_d) or is_key(event, pygame.K_RIGHT): moving_right = True
                if is_key(event, pygame.K_SPACE): shoot = True
                if is_key(event, pygame.K_q): grenade = True
                if (is_key(event, pygame.K_w) or is_key(event, pygame.K_UP)) and self.player.alive: self.player.jump = True
                if is_key(event, pygame.K_ESCAPE):
                    if (self.player.alive and start_game): pause_game = not pause_game
            # Releases
            if event.type == pygame.KEYUP:
                if is_key(event, pygame.K_a) or is_key(event, pygame.K_LEFT): moving_left = False
                if is_key(event, pygame.K_d) or is_key(event, pygame.K_RIGHT): moving_right = False
                if is_key(event, pygame.K_SPACE): shoot = False
                if is_key(event, pygame.K_q):
                    grenade = False
                    grenade_thrown = False
                if (is_key(event, pygame.K_w) or is_key(event, pygame.K_UP)) and self.player.alive: self.player.jump = False

    def run(self):
        global start_game, pause_game, bg_scroll, screen_scroll, shoot, bullet_group, shot_fx, \
              grenade, grenade_thrown, level_complete, moving_left, moving_right, \
              score_database, update_console_cooldown, show_settings_menu, show_fps, show_enemy_healthbar, intro_fade
        print('[GameManager] Running...')
        while self.running:
            clock.tick(FPS)
            screen.fill(BLACK)

            if update_console_cooldown == 0:
                update_console_cooldown = 11
                if start_game: show_console_information(self.level, level_complete, pause_game, self.player, score_database)

            if (MAX_LEVELS == 0):
                draw_text("No Levels found", font, WHITE, SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2)
                draw_text("Please build your own level with level_editor.py", font, WHITE, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 30)
            elif show_settings_menu: show_settings_menu, show_fps, show_enemy_healthbar = show_settings(show_settings_menu, show_fps, show_enemy_healthbar)
            elif not start_game: start_game, start_intro, show_settings_menu = show_start_menu(self.exit_game, show_settings_menu)
            elif pause_game: show_settings_menu, self.player, self.health_bar, self.world, self.world_data, pause_game, self.level, intro_fade = show_pause_menu(show_settings_menu, self.exit_game, self.world, self.world_data, self.player, self.health_bar, self.level, intro_fade)
            else:
                update_player(font, self.player, self.world, bg_scroll, screen_scroll, self.health_bar, show_enemy_healthbar)

                for enemy in enemy_group:
                    enemy.ai(self.world, self.player, bullet_group, screen_scroll, bg_scroll, water_group, exit_group, shot_fx, screen)
                    enemy.update(screen, self.player, show_enemy_healthbar)
                    enemy.draw()

                update_pygame_groups(screen, self.world, self.player, screen_scroll, grenade_fx)

                # Show intro
                if start_intro:
                    if intro_fade.fade(screen):
                        start_intro = False
                        intro_fade.fade_counter = 0

                if self.player.alive:
                    # Shoot bullets
                    if shoot: self.player.shoot(bullet_group, shot_fx)
                    # Throw grenades
                    elif grenade and not grenade_thrown and self.player.grenades > 0:
                        grenade = Grenade(
                            self.player.rect.centerx + (0.5 * self.player.rect.size[0] * self.player.direction),
                            self.player.rect.top, self.player.direction
                        )
                        grenade_group.add(grenade)
                        # Reduce Grenades
                        self.player.grenades -= 1
			
                        grenade_thrown = True
                    # Jump
                    if self.player.in_air:
                        if walking_fx.get_num_channels() > 0: walking_fx.stop()
                        self.player.update_action(ActionType.JUMP)
                    # Move
                    elif moving_left or moving_right:
                        if walking_fx.get_num_channels() == 0: walking_fx.play()
                        self.player.update_action(ActionType.RUN)
                    # Idle
                    else:
                        if walking_fx.get_num_channels() > 0: walking_fx.stop()
                        self.player.update_action(ActionType.IDLE)
                    screen_scroll, level_complete = self.player.move(self.world, moving_left, moving_right, bg_scroll, water_group, exit_group)
                    bg_scroll -= screen_scroll
                    # Check if self.player completed level
                    if level_complete:
                        if self.level < MAX_LEVELS:
                            self.level += 1
                            score_database += self.player.score
                            start_intro = True
                            screen_scroll = 0
                            bg_scroll = 0
                            self.world_data = reset_level()
                            self.world_data = load_level(self.level, self.world_data)
                            self.world = World()
                            self.player, self.health_bar = self.world.process_data(screen, self.world_data, enemy_group, item_box_group,
                                                                    decoration_group, water_group,
                                                                    exit_group)
                        else:
                            if complete_fade.fade(screen):
                                if restart_button.draw(screen):
                                    bg_scroll = 0
                                    screen_scroll = 0
                                    self.level = 1
                                    self.world_data = reset_level()
                                    self.world_data = load_level(self.level, self.world_data)
                                    self.world = World()
                                    self.player, self.health_bar = self.world.process_data(screen, self.world_data, enemy_group, item_box_group,
                                                                            decoration_group, water_group, exit_group)
                                    start_intro = True
                            

                else:
                    screen_scroll = 0
                    if death_fade.fade(screen):
                        if restart_button.draw(screen):
                            bg_scroll = 0
                            intro_fade.fade_counter = 0
                            death_fade.fade_counter = 0
                            self.world_data = reset_level()
                            self.world_data = load_level(self.level, self.world_data)
                            self.world = World()
                            self.player, self.health_bar = self.world.process_data(screen, self.world_data, enemy_group, item_box_group,
                                                                    decoration_group, water_group,
                                                                    exit_group)
                            start_intro = True
            update_console_cooldown -= 1
            
            if show_fps: draw_text(f"FPS: {round(clock.get_fps())}", font, WHITE, SCREEN_WIDTH - 110, 25)

            self.listen_events()

            pygame.display.update()
if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.run()
    pygame.quit()
