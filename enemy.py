import random

import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self,SW_game):
        super().__init__()

            # 获取游戏屏幕对象和设置对象
        self.screen = SW_game.screen
        self.settings = SW_game.settings
        self.screen_rect = SW_game.screen.get_rect()

        self.get_enemy_type()

        self.health = self.settings.enemy_health[self.enemy_type]

        self.image_config = {'dive':{'font':pygame.font.SysFont(None,80),'str':'v'},
                            'sweep':{'font':pygame.font.SysFont(None,90),'str':'<>'},
                            'tank':{'font':pygame.font.SysFont(None,100),'str':f'<[{self.health}]>'}}
        
        self.all_enemy_image = {}

        for type,config in self.image_config.items():
            enemy_type = type
            self.enemy_font = config['font']
            self.enemy_image_str = config['str']
            self.enemy_image = self.enemy_font.render(self.enemy_image_str,True,self.settings.enemy_color)
            self.all_enemy_image[enemy_type] = self.enemy_image

            # 加载敌机图像并获取其外接矩形
        self.image = self.all_enemy_image[self.enemy_type]
        self.rect = self.image.get_rect()

            # 敌机速度
        self.y_speed = self.settings.enemy_y_speed[self.enemy_type]
        self.x_speed = random.choice([-self.settings.enemy_x_speed[self.enemy_type], self.settings.enemy_x_speed[self.enemy_type]])

            # 这是将敌机坐标转换为小数，以便更精确地控制敌机的移动
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

            # 敌机刷新间隔
        self.enemy_spawn_delay = SW_game.stats.enemy_spawn_delay

        # 更新敌机位置
    def update(self):
        self.y += self.y_speed
        if self.enemy_type == 'tank':
            if self.y < 0 or self.y > self.screen_rect.height - self.rect.height:
                self.y_speed = -self.y_speed
        self.rect.y = self.y
        self.x += self.x_speed
        if self.x < 0 or self.x > self.screen_rect.width - self.rect.width:
            self.x_speed = -self.x_speed
        self.rect.x = self.x

        # 增加敌人速度
    def speedup(self,difficulty=0):
        if self.enemy_type == 'tank':
            self.y_speed += self.settings.enemy_y_speed_up*difficulty*0.5
        self.y_speed += self.settings.enemy_y_speed_up*difficulty
        if self.enemy_type != 'dive':
            if self.enemy_type == 'tank':
                self.x_speed += self.settings.enemy_x_speed_up*difficulty*0.5
            self.x_speed += self.settings.enemy_x_speed_up*difficulty

        # 生成随机敌人
    def get_enemy_type(self):
        i = random.randint(1,100)
        if i <= 50:
            self.enemy_type = 'dive'
        elif i <= 85:
            self.enemy_type = 'sweep'
        elif i <= 100:
            self.enemy_type = 'tank'


class Boss(Enemy):

    def __init__(self, SW_game,boss_type):
        super().__init__(SW_game)

        self.stats = SW_game.stats
        self.boss_type = boss_type
        
        self.health = self.settings.boss_health[self.boss_type]


        self.image_config = {'alpha':{'font':pygame.font.SysFont(None,200),'str':'\[v|V|v]/'},
                            'beta':{'font':pygame.font.SysFont(None,300),'str':'<[***#*>V<*#***]>'},
                            'gamma':{'font':pygame.font.SysFont(None,250),'str':'\[⚙[V#*#V]⚙]/'}}
        
        self.all_boss_image = {}

        for type,config in self.image_config.items():
            boss_type = type
            self.boss_font = config['font']
            self.boss_image_str = config['str']
            self.boss_image = self.boss_font.render(self.boss_image_str,True,self.settings.boss_color)
            self.all_boss_image[boss_type] = self.boss_image

        self.y_speed = self.settings.boss_y_speed[self.boss_type]
        self.x_speed = random.choice([-self.settings.boss_x_speed[self.boss_type], self.settings.boss_x_speed[self.boss_type]])

    def get_enemy_type(self):
        pass

    def speedup(self,difficulty=0):
        pass