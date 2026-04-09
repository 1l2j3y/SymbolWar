import pygame
    # 用于储存会随邮寄的进行而动态变化的数据
class GameStats:

    def __init__(self, PW_game):
        self.settings = PW_game.settings
        self.screen = PW_game.screen
        self.screen_rect = self.screen.get_rect()
        self.plane = PW_game.plane
        self.enemies = PW_game.enemies
        self.bullets = PW_game.bullets
        
        self.highest_score = 0
        self.reset_stats()
        self.game_active = False
        # 重置统计数据
    def reset_stats(self):
        self.score = 0
        self.difficulty = 0
        self.plane.health = self.settings.plane_health
        self.enemy_spawn_delay = self.settings.enemy_spawn_delay
        self.max_enemies =  self.settings.max_enemies

        # 清空子弹和敌机
        self.enemies.empty()
        self.bullets.empty()
        # 令飞机重新居中            
        self.plane.rect.midbottom = self.screen_rect.midbottom
        # 令游戏更新为活动状态
        self.game_active = True
        # 重置游戏开始时间
        self.game_start_time = pygame.time.get_ticks()