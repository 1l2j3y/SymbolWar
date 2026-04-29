import sys
import json
import random

import pygame

from settings import Settings
from plane import Plane
from enemy import Enemy,Boss
from stats import GameStats
from button import Button
from gui import Gui

class SymbolWar:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
            # 创建游戏屏幕对象
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
            # 创建设置对象
        self.settings = Settings()
        self.screen_rect = self.screen.get_rect()
        self.settings.zoom_bg_image(self.screen_rect)
        pygame.display.set_caption("Plane War")
        self.bg_color = (self.settings.bg_color)
            # 创建飞机对象、子弹编组和敌机编组
        self.plane1 = Plane(self)
        self.plane2 = Plane(self, player_id=2)
        self.planes = pygame.sprite.Group(self.plane1, self.plane2)
        self.bullets1 = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.boss = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.gui = Gui(self)
        self.play_button = Button(self,'Play')
        self.help_button = Button(self,'Help',100)
        self.coop_button = Button(self,'Co-op',200)
        self.vs_button = Button(self,'VS',300)
        self.keydown = {pygame.K_RIGHT:(self.plane1, 'moving_right', True),
                        pygame.K_LEFT:(self.plane1, 'moving_left', True),
                        pygame.K_UP:(self.plane1, 'moving_up', True),
                        pygame.K_DOWN:(self.plane1, 'moving_down', True),
                        pygame.K_a:(self.plane2, 'moving_left', True),
                        pygame.K_d:(self.plane2, 'moving_right', True),
                        pygame.K_w:(self.plane2, 'moving_up', True),
                        pygame.K_s:(self.plane2, 'moving_down', True)}
        self.keyup = {pygame.K_RIGHT:(self.plane1, 'moving_right', False),
                      pygame.K_LEFT:(self.plane1, 'moving_left', False),
                      pygame.K_UP:(self.plane1, 'moving_up', False),
                      pygame.K_DOWN:(self.plane1, 'moving_down', False),
                      pygame.K_a:(self.plane2, 'moving_left', False),
                      pygame.K_d:(self.plane2, 'moving_right', False),
                      pygame.K_w:(self.plane2, 'moving_up', False),
                      pygame.K_s:(self.plane2, 'moving_down', False)}
        self.password = ''
            # 敌机生成计时器
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.boss_spawn_time = 24000

        self.clock = pygame.time.Clock()


        # 检测键鼠事件
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("highest.json","w",encoding="utf-8") as f:
                    json.dump(self.stats.highest_score,f,indent=2)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event) 
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)

        # 检测键盘按键事件类型
    def _check_keydown_events(self, event):
        for keydown,kd_event in self.keydown.items():
            if event.key == keydown:
                plane, attr, value = kd_event
                setattr(plane, attr, value)
        if event.key == pygame.K_SPACE:
            self.plane1.shoot_bullet(self.bullets1)  
        elif event.key == pygame.K_f:
            self.plane2.shoot_bullet(self.bullets2)
        elif event.key == pygame.K_ESCAPE:
            with open("highest.json","w",encoding="utf-8") as f:
                json.dump(self.stats.highest_score,f,indent=2)
            sys.exit()
        if not self.stats.game_active:
            if event.key in (pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9):
                self.password += event.unicode
            elif event.key == pygame.K_RETURN:
                if self.password == '114514':
                    self.settings.help_text_lines = self.settings.help_text_ch
                    self.password = ''
                    self.settings.translate_sound.play()
                
        # 检测键盘松键事件类型
    def _check_keyup_events(self, event):
        for keyup,ku_event in self.keyup.items():
            if event.key == keyup:
                plane, attr, value = ku_event
                setattr(plane, attr, value)
        # 检测开始按钮并进行初始化
    def _check_button(self,mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.gui.score_GUI_create()
            self.gui.plane1_health_GUI_create(self.plane1)
        if self.help_button.rect.collidepoint(mouse_pos) and not self.stats.game_active and not self.stats.help_show:
            self.stats.help_show = True
        if not self.help_button.rect.collidepoint(mouse_pos) and not self.stats.game_active and self.stats.help_show:
            self.stats.help_show = False
        if self.coop_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.gui.score_GUI_create()
            self.gui.plane1_health_GUI_create(self.plane1)
            self.gui.plane2_health_GUI_create(self.plane2,50)
            self.stats.coop = True
        if self.vs_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.gui.score_GUI_create()
            self.gui.plane1_health_GUI_create(self.plane1)
            self.gui.plane2_health_GUI_create(self.plane2,50)
            self.stats.vs = True
            self.plane2.rect.midtop = self.screen_rect.midtop
            self.plane2.image = self.settings.reverse_plane_image
            self.settings.bullet_speed += 10
            self.settings.plane_speed -= 5

        # 更新子弹位置并检测与敌机的碰撞
    def _check_bullet_enemy_collisions(self):
        self.bullets1.update()
        self.bullets2.update()
        for bullet in self.bullets1.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen_rect.height:
                self.bullets1.remove(bullet)
        for bullet in self.bullets2.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen_rect.height:
                self.bullets2.remove(bullet)
            # 检查子弹和敌机之间的碰撞
        enemy_collisions1 = pygame.sprite.groupcollide(self.bullets1, self.enemies, True, False)
        boss_collisions1 = pygame.sprite.groupcollide(self.bullets1, self.boss, True, False)
        enemy_collisions2 = pygame.sprite.groupcollide(self.bullets2, self.enemies, True, False)
        boss_collisions2 = pygame.sprite.groupcollide(self.bullets2, self.boss, True, False)
        self._process_collisions(enemy_collisions1)
        self._process_collisions(boss_collisions1, is_boss=True)
        self._process_collisions(enemy_collisions2)
        self._process_collisions(boss_collisions2, is_boss=True)
    
    def _process_collisions(self, collisions, is_boss=False):
        for hit_enemies in collisions.values():
            for injured_enemy in hit_enemies:
                injured_enemy.health -= 1
                injured_enemy.update_image()
                if injured_enemy.health <= 0:
                    injured_enemy.kill()
                    if not is_boss:
                        self.settings.enemy_killed_sound.play()
                        self.stats.score += self.settings.enemy_points[injured_enemy.type]
                    else:
                        self.settings.boss_killed_sound.play()
                        self.stats.score += self.settings.boss_points
                        self.boss_bullets.empty()
                        self.stats.boss_exist = False
                        pygame.mixer.music.load(self.settings.bgm_path)
                        pygame.mixer.music.play(-1)
                if self.stats.score > self.stats.highest_score:
                    self.stats.highest_score = self.stats.score
                self.gui.score_GUI_create() 
        # 创建敌机
    def create_enemy(self):
        self._create_boss()
        if self.stats.boss_exist:
            return
        if self.stats.vs:
            return
        now_time = pygame.time.get_ticks()
        now_difficulty = (now_time - self.stats.game_start_time) // self.settings.difficulty_up_delay
        self.gui.difficulty_GUI_create()

        if now_difficulty > self.stats.difficulty:
            if self.stats.enemy_spawn_delay > self.settings.enemy_spawn_min_delay:
                self.stats.enemy_spawn_delay *= self.settings.enemy_spawn_delay_down_coefficient
            self.stats.max_enemies += self.settings.enemy_maxnum_up
            self.stats.difficulty = now_difficulty

        if len(self.enemies) < self.stats.max_enemies:
            if now_time - self.last_enemy_spawn_time < self.stats.enemy_spawn_delay:
                return
            self.last_enemy_spawn_time = now_time
            new_enemy = Enemy(self)
            new_enemy.speedup(now_difficulty)
            self.enemies.add(new_enemy)

        # 创建boss
    def _create_boss(self):
        if self.stats.boss_exist:
            return
        now_time = pygame.time.get_ticks() - self.stats.game_start_time
        boss_type = None
        if self.stats.score >= 1000 and now_time >= 60000 and not self.stats.boss_spawned['alpha']:
            boss_type = 'alpha'
            self.stats.boss_spawned['alpha'] = True
        if self.stats.score >= 3000 and now_time >= 120000 and not self.stats.boss_spawned['beta']:
            boss_type = 'beta'
            self.stats.boss_spawned['beta'] = True
        if self.stats.score >= 5000 and now_time >= 180000 and not self.stats.boss_spawned['gamma']:
            boss_type = 'gamma'
            self.stats.boss_spawned['gamma'] = True
        if now_time >= self.boss_spawn_time and all(self.stats.boss_spawned.values()):
            boss_type = random.choice(['alpha','beta','gamma'])
            self.boss_spawn_time += 60000

        if boss_type:
            new_boss = Boss(self,boss_type)
            self.boss.add(new_boss)
            self.stats.boss_exist = True
            self.enemies.empty()
            self.bullets1.empty()
            self.bullets2.empty()
            self.boss_bullets.empty()
            pygame.mixer.music.load(self.settings.boss_bgm_path)
            pygame.mixer.music.play(-1)

        # 更新敌机位置并删除已消失的敌机
    def _update_enemies(self):
        self.enemies.update()
        self.boss.update()

        self._check_plane_hit_collisions()

        for enemy in self.enemies.copy():
            if enemy.rect.top >= self.screen.get_rect().height:
                self.enemies.remove(enemy)

        # 检查飞机受击的碰撞
    def _check_plane_hit_collisions(self):
        if self.stats.coop:
            plane_to_remove = []
            for plane in self.planes:
                collisions_enemy = pygame.sprite.spritecollideany(plane, self.enemies)
                collisions_boss = pygame.sprite.spritecollideany(plane, self.boss)
                collisions_boss_bullet = pygame.sprite.spritecollideany(plane, self.boss_bullets)
                if (collisions_enemy or collisions_boss or collisions_boss_bullet) and not plane.invincible:
                    self.settings.plane_hit_sound.play()
                    if collisions_enemy is not None:
                        self.enemies.remove(collisions_enemy)
                    if collisions_boss_bullet is not None:
                        self.boss_bullets.remove(collisions_boss_bullet)
                    plane.health -= 1
                    if plane.health <= 0:
                        plane_to_remove.append(plane)
                    # 飞机进入无敌状态
                    plane.invincible = True
                    plane.invincibility_start_time = pygame.time.get_ticks()
            for plane in plane_to_remove:
                plane.kill()
        elif self.stats.vs:
            collisions_plane = pygame.sprite.collide_rect(self.plane1, self.plane2)
            if collisions_plane and not self.plane1.invincible and not self.plane2.invincible:
                if self.plane1.health > 0 and self.plane2.health > 0:
                    self.settings.plane_hit_sound.play()
                    self.plane1.health -= 1
                    self.plane2.health -= 1
                    # 飞机进入无敌状态
                    self.plane1.invincible = True
                    self.plane1.invincibility_start_time = pygame.time.get_ticks()
                    self.plane2.invincible = True
                    self.plane2.invincibility_start_time = pygame.time.get_ticks()
            collisions_plane_bullet1= pygame.sprite.spritecollideany(self.plane1, self.bullets2)
            collisions_plane_bullet2= pygame.sprite.spritecollideany(self.plane2, self.bullets1)
            if collisions_plane_bullet1 and not self.plane1.invincible:
                self.settings.plane_hit_sound.play()
                self.plane1.health -= 1
                # 飞机进入无敌状态
                self.plane1.invincible = True
                self.plane1.invincibility_start_time = pygame.time.get_ticks()
            if collisions_plane_bullet2 and not self.plane2.invincible:
                self.settings.plane_hit_sound.play()
                self.plane2.health -= 1
                # 飞机进入无敌状态
                self.plane2.invincible = True
                self.plane2.invincibility_start_time = pygame.time.get_ticks()
        else:
            collisions_enemy = pygame.sprite.spritecollideany(self.plane1, self.enemies)
            collisions_boss = pygame.sprite.spritecollideany(self.plane1, self.boss)
            collisions_boss_bullet = pygame.sprite.spritecollideany(self.plane1, self.boss_bullets)
            if (collisions_enemy or collisions_boss or collisions_boss_bullet) and not self.plane1.invincible:
                self.settings.plane_hit_sound.play()
                if collisions_enemy is not None:
                    self.enemies.remove(collisions_enemy)
                if collisions_boss_bullet is not None:
                    self.boss_bullets.remove(collisions_boss_bullet)
                self.plane1.health -= 1
                # 飞机进入无敌状态
                self.plane1.invincible = True
                self.plane1.invincibility_start_time = pygame.time.get_ticks()
        
        # 检查游戏结束
    def _check_game_over(self):
        if self.stats.coop:
            gameover = self.plane1.health <= 0 and self.plane2.health <= 0
        elif self.stats.vs:
            gameover = self.plane1.health <= 0 or self.plane2.health <= 0
        else:
            gameover = self.plane1.health <= 0
        if gameover:
            self.settings.game_over_sound.play()
            self.stats.game_active = False

        # 飞机闪烁绘制
    def plane_blink_draw(self):
        if self.stats.coop or self.stats.vs:
            for plane in self.planes:
                self._check_plane_invincibility(plane)
                if self._plane_blink(plane):
                    plane.plane_draw()
        else:
            self._check_plane_invincibility(self.plane1)
            if self._plane_blink(self.plane1):
                self.plane1.plane_draw()
        # 检查飞机无敌状态
    def _check_plane_invincibility(self, plane):
        if plane.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - plane.invincibility_start_time >= plane.invincibility_duration:
                plane.invincible = False
        # 飞机闪烁效果
    def _plane_blink(self, plane):
        if plane.invincible:
            now_time = pygame.time.get_ticks()
            if (now_time - plane.invincibility_start_time) // self.settings.plane_blink_time % 2 == 0:
                return True
            return False
        return True

        # 刷新屏幕
    def update_screen(self):
        self.screen.blit(self.settings.bg_image,(0,self.settings.bg_y1))
        self.screen.blit(self.settings.bg_image,(0,self.settings.bg_y2))
        self.plane_blink_draw()
        if self.stats.coop or self.stats.vs:
            self.gui.plane1_health_GUI_create(self.plane1)
            self.gui.plane2_health_GUI_create(self.plane2,50)
            self.gui.small_plane2s.draw(self.screen)
        else:
            self.gui.plane1_health_GUI_create(self.plane1)
        self.gui.draw()
        self.bullets1.draw(self.screen)
        self.bullets2.draw(self.screen)
        self.enemies.draw(self.screen)
        self.draw_help()
        if self.stats.boss_exist:
            boss = self.boss.sprites()[0]
            self.boss.draw(self.screen)
            self.gui.boss_health_GUI_create(boss)
            self.boss_bullets.update()
            self.boss_bullets.draw(self.screen)
        if not self.stats.game_active:
            self.help_button.button_draw()
            self.play_button.button_draw()
            self.coop_button.button_draw()
            self.vs_button.button_draw()
            
        pygame.display.flip()
        # 背景滚动
    def _bg_scroll(self):
        scroll_speed = self.settings.bg_scroll_speed
        self.settings.bg_y1 += scroll_speed
        self.settings.bg_y2 += scroll_speed
        if self.settings.bg_y1 > self.screen_rect.height:
           self.settings.bg_y1 = -self.screen_rect.height
        if self.settings.bg_y2 > self.screen_rect.height:
           self.settings.bg_y2 = -self.screen_rect.height

    def draw_help(self):
        if self.stats.help_show:
            self.screen.blit(self.settings.help_window, (0, 0))
            self.settings.help_text_title_rect.centerx = self.settings.help_window_rect.centerx
            self.screen.blit(self.settings.help_text_title_image, self.settings.help_text_title_rect)
            text_y = 30 + self.settings.help_text_title_rect.height
            for line in self.settings.help_text_lines:
                help_text_image = self.settings.help_text_font.render(line, True, self.settings.help_text_color)
                help_text_rect = help_text_image.get_rect()
                help_text_rect.x = 20
                help_text_rect.y = text_y
                self.screen.blit(help_text_image, help_text_rect)
                text_y += 30

        # 游戏主循环
    def run_game(self):
            while True:
                self.check_events()
                self.update_screen()
                if self.stats.game_active:
                    pygame.mouse.set_visible(False)
                    break
                else:
                    pygame.mouse.set_visible(True)

            pygame.mixer.music.load(self.settings.bgm_path)
            pygame.mixer.music.set_volume(self.settings.bgm_volume)
            pygame.mixer.music.play(-1)

            while True:
                self.check_events()
                self.planes.update()
                self._check_bullet_enemy_collisions()
                self.create_enemy()
                self._update_enemies()
                self._bg_scroll()
                self._check_game_over()
                if not self.stats.game_active:
                    break
                self.update_screen()
                self.clock.tick(60)

if __name__ == "__main__":
    symbol_war = SymbolWar()
    while True:
        symbol_war.run_game()