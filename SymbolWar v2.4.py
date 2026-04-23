import sys
import json

import pygame

import enemy
from settings import Settings
from plane import Plane
from bullet import Bullet
from enemy import Enemy,Boss
from stats import GameStats
from button import Button
from gui import Gui

class SymbolWar:
    
    def __init__(self):
        pygame.init()
            # 创建设置对象
        self.settings = Settings()
            # 创建游戏屏幕对象， 并对屏幕进行一些调整
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height
        pygame.display.set_caption("Plane War")
        self.bg_color = (self.settings.bg_color)
            # 创建飞机对象、子弹编组和敌机编组
        self.plane = Plane(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.boss = pygame.sprite.Group()
        self.gui = Gui(self)
        self.button = Button(self,'Play')
            # 敌机生成计时器
        self.last_enemy_spawn_time = pygame.time.get_ticks()


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
                self._check_play_button(mouse_pos)
        # 检测键盘按键事件类型
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.plane.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.plane.moving_left = True
        elif event.key == pygame.K_UP:
            self.plane.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.plane.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            with open("highest.json","w",encoding="utf-8") as f:
                json.dump(self.stats.highest_score,f,indent=2)
            sys.exit()
        # 检测键盘松键事件类型
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.plane.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.plane.moving_left = False
        elif event.key == pygame.K_UP:
            self.plane.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.plane.moving_down = False
        # 检测开始按钮并进行初始化
    def _check_play_button(self,mouse_pos):
        if self.button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.gui.score_GUI_create()
            self.gui.image_GUI_create()


        # 开火
    def fire_bullet(self):
        if len(self.bullets) < self.settings.max_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

        # 更新子弹位置并检测与敌机的碰撞
    def _check_bullet_enemy_collisions(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # 检查子弹和敌机之间的碰撞
        enemy_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for hit_enemies in enemy_collisions.values():
            for injured_enemy in hit_enemies:
                injured_enemy.health -= 1
                if injured_enemy.health <= 0:
                    injured_enemy.kill()
                    self.stats.score += self.settings.enemy_points[injured_enemy.enemy_type]
                if self.stats.score > self.stats.highest_score:
                    self.stats.highest_score = self.stats.score
                self.gui.score_GUI_create()

        boss_collisions = pygame.sprite.groupcollide(self.bullets, self.boss, True, False)
        for hit_boss in boss_collisions.values():
            for injured_boss in hit_boss:
                injured_boss.health -= 1
                if injured_boss.health <= 0:
                    injured_boss.kill()
                    self.stats.score += self.settings.boss_points
                    self.stats.boss_exist = False
                    if self.stats.score > self.stats.highest_score:
                        self.stats.highest_score = self.stats.score
                    self.gui.score_GUI_create()
        

        # 创建敌机
    def create_enemy(self):
        self._create_boss()
        if self.stats.boss_exist:
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

        if boss_type:
            new_boss = Boss(self,boss_type)
            self.boss.add(new_boss)
            self.stats.boss_exist = True

        # 更新敌机位置并删除已消失的敌机
    def _update_enemies(self):
        self.enemies.update()
        self.boss.update()

        self._check_plane_enemy_collisions()
        self._check_plane_boss_collisions()

        for enemy in self.enemies.copy():
            if enemy.rect.top >= self.screen.get_rect().height:
                self.enemies.remove(enemy)

        # 检查敌机和飞机之间的碰撞
    def _check_plane_enemy_collisions(self):
        collisions_enemy = pygame.sprite.spritecollideany(self.plane, self.enemies)
        if collisions_enemy and not self.plane.invincible:
            print("Plane hit!")
            self.enemies.remove(collisions_enemy)
            self.plane.health -= 1
            self.gui.image_GUI_create()
                # 飞机进入无敌状态
            self.plane.invincible = True
            self.plane.invincibility_start_time = pygame.time.get_ticks()
                # 检查游戏结束
            if self.plane.health <= 0:
                print("Game Over!")
                self.stats.game_active = False

        # 检查boss和飞机之间的碰撞
    def _check_plane_boss_collisions(self):
        collisions_boss = pygame.sprite.spritecollideany(self.plane, self.boss)
        if collisions_boss and not self.plane.invincible:
            print("Plane hit!")
            self.plane.health -= 1
            self.gui.image_GUI_create()
                # 飞机进入无敌状态
            self.plane.invincible = True
            self.plane.invincibility_start_time = pygame.time.get_ticks()
                # 检查游戏结束
            if self.plane.health <= 0:
                print("Game Over!")
                self.stats.game_active = False


        # 飞机闪烁绘制
    def plane_blink_draw(self):
        self._check_plane_invincibility()
        if self._plane_blink():
            self.plane.plane_draw()
        # 检查飞机无敌状态
    def _check_plane_invincibility(self):
        if self.plane.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.plane.invincibility_start_time >= self.plane.invincibility_duration:
                self.plane.invincible = False
        # 飞机闪烁效果
    def _plane_blink(self):
        if self.plane.invincible:
            now_time = pygame.time.get_ticks()
            if (now_time - self.plane.invincibility_start_time) // self.settings.plane_blink_time % 2 == 0:
                return True
            return False
        return True    

        # 刷新屏幕
    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.plane_blink_draw()
        self.gui.draw()
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.boss.draw(self.screen)
        if not self.stats.game_active:
            self.button.button_draw()
        pygame.display.flip()

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

            while True:
                self.check_events()
                self.plane.update()
                self._check_bullet_enemy_collisions()
                self.create_enemy()
                self._update_enemies()
                if not self.stats.game_active:
                    break
                self.update_screen()

if __name__ == "__main__":
    symbol_war = SymbolWar()
    while True:
        symbol_war.run_game()