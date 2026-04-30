import json
import sys
import pygame
from pathlib import Path

def data_path(filename):
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / filename
    else:
        return Path(__file__).parent / filename

    # 用于储存会随游戏的进行而动态变化的数据
class GameStats:

    def __init__(self, SW_game):
        self.settings = SW_game.settings
        self.screen = SW_game.screen
        self.screen_rect = self.screen.get_rect()
        self.plane1 = SW_game.plane1
        self.plane2 = SW_game.plane2
        self.planes = SW_game.planes
        self.enemies = SW_game.enemies
        self.bullets1 = SW_game.bullets1
        self.bullets2 = SW_game.bullets2
        try:
            with open(data_path("highest.json"), "r", encoding="utf-8") as f:
                self.highest_score = json.load(f)
        except FileNotFoundError:
            self.highest_score = 0
        self.reset_stats()
        self.game_active = False
        
        # 重置统计数据
    def reset_stats(self):
        self.score = 0
        self.difficulty = 0
        self.plane1.health = self.settings.plane_health
        self.plane2.health = self.settings.plane_health
        self.enemy_spawn_delay = self.settings.enemy_spawn_delay
        self.max_enemies =  self.settings.max_enemies
        self.boss_spawned = {'alpha':False,'beta':False,'gamma':False}
        self.boss_exist = False
        self.help_show = False
        self.coop = False
        self.vs = False

        # 清空子弹和敌机
        self.enemies.empty()
        self.bullets1.empty()
        self.bullets2.empty()
        # 重置飞机位置和状态
        if self.plane1 not in self.planes and self.plane2 not in self.planes:
            self.planes.add(self.plane1)
            self.planes.add(self.plane2)
        self.plane1.rect.midbottom = self.screen_rect.midbottom
        self.plane2.rect.midbottom = self.screen_rect.midbottom
        self.plane1.invincible = False
        self.plane2.invincible = False
        self.plane2.image = self.settings.plane_image
        # 令游戏更新为活动状态
        self.game_active = True
        # 重置游戏开始时间
        self.game_start_time = pygame.time.get_ticks()
        self.random_boss_spawned_time = 240000