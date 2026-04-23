import random

import pygame
from pygame.sprite import Sprite

from bullet import BossBullet

class Enemy(Sprite):

    def __init__(self,SW_game):
        super().__init__()

            # 获取游戏屏幕对象和设置对象
        self.screen = SW_game.screen
        self.settings = SW_game.settings
        self.screen_rect = SW_game.screen.get_rect()
            # 生成随机敌人类型
        self.get_type()
            # 根据敌人类型设置敌人生命值
        self.health = self.settings.enemy_health[self.type]
            # 根据敌人类型设置敌人图像,获取敌人素材库(这个素材库中的图像只是被拿来用的素材,并不是最终的敌人图像,这个素材库类似settings的对应设置)
        self.image_config = {'dive':{'font':pygame.font.SysFont(None,80),'str':'v'},
                            'sweep':{'font':pygame.font.SysFont(None,90),'str':'<>'},
                            'tank':{'font':pygame.font.SysFont(None,100),'str':f'<[{self.health}]>'}}
        
        self.all_enemy_image = {}

        for type,config in self.image_config.items():
            type = type
            self.enemy_font = config['font']
            self.enemy_image_str = config['str']
            self.enemy_image = self.enemy_font.render(self.enemy_image_str,True,self.settings.enemy_color)
            self.all_enemy_image[type] = self.enemy_image

            # 加载敌机图像并获取其外接矩形(这个图像是最终的敌人图像,它是根据敌人类型和敌人生命值动态生成的)
        self.image = self.all_enemy_image[self.type]
        self.rect = self.image.get_rect()

            # 敌机速度
        self.y_speed = self.settings.enemy_y_speed[self.type]
        self.x_speed = random.choice([-self.settings.enemy_x_speed[self.type], self.settings.enemy_x_speed[self.type]])

            # 这是将敌机坐标转换为小数，以便更精确地控制敌机的移动
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

            # 敌机刷新间隔
        self.enemy_spawn_delay = SW_game.stats.enemy_spawn_delay

        # 更新敌机位置
    def update(self):
        self.y += self.y_speed
        if self.type == 'tank':
            if self.y < 0 or self.y > self.screen_rect.height - self.rect.height:
                self.y_speed = -self.y_speed
        self.rect.y = self.y
        self.x += self.x_speed
        if self.x < 0 or self.x > self.screen_rect.width - self.rect.width:
            self.x_speed = -self.x_speed
        self.rect.x = self.x

    def update_image(self):
        for type,config in self.image_config.items():
            enemy_font = config['font']
            if type == 'tank':
                text = f'<[{self.health}]>'
                self.image = enemy_font.render(text,True,self.settings.enemy_color)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

        # 增加敌人速度
    def speedup(self,difficulty=0):
        if self.type == 'tank':
            self.y_speed += self.settings.enemy_y_speed_up*difficulty*0.5
        self.y_speed += self.settings.enemy_y_speed_up*difficulty
        if self.type != 'dive':
            if self.type == 'tank':
                self.x_speed += self.settings.enemy_x_speed_up*difficulty*0.5
            self.x_speed += self.settings.enemy_x_speed_up*difficulty

        # 生成随机敌人
    def get_type(self):
        i = random.randint(1,100)
        if i <= 50:
            self.type = 'dive'
        elif i <= 90:
            self.type = 'sweep'
        elif i <= 100:
            self.type = 'tank'


class Boss(Sprite):

    def __init__(self, SW_game,type):
        super().__init__()

            # 获取游戏屏幕对象和设置对象
        self.SW_game = SW_game
        self.screen = SW_game.screen
        self.settings = SW_game.settings
        self.screen_rect = SW_game.screen.get_rect()

        self.type = type

        self.health = self.settings.boss_health[self.type]

        self.image_config = {'alpha':{'font':pygame.font.SysFont(None,200),'str':'\\[v|V|v]/'},
                            'beta':{'font':pygame.font.SysFont(None,300),'str':'<[***#*>V<*#***]>'},
                            'gamma':{'font':pygame.font.SysFont(None,250),'str':'\\[⚙[V#*#V]⚙]/'}}
        
        self.all_boss_image = {}

        for type,config in self.image_config.items():
            type = type
            self.boss_font = config['font']
            self.boss_image_str = config['str']
            self.boss_image = self.boss_font.render(self.boss_image_str,True,self.settings.boss_color)
            self.all_boss_image[type] = self.boss_image

            # 加载boss图像并获取其外接矩形
        self.image = self.all_boss_image[self.type]
        self.rect = self.image.get_rect()

        self.y_speed = self.settings.boss_y_speed[self.type]
        self.x_speed = random.choice([-self.settings.boss_x_speed[self.type], self.settings.boss_x_speed[self.type]])

        self.shoot_delay = self.settings.boss_shoot_delay[self.type]
        self.last_shoot_time = 0

            # 这是将boss坐标转换为小数，以便更精确地控制boss的移动
        self.rect.y = 100
        self.rect.centerx = self.screen_rect.centerx
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    # 更新boss和boss子弹位置
    def update(self):
        self.y += self.y_speed
        self.rect.y = self.y
        self.x += self.x_speed
        if self.x < 0 or self.x > self.screen_rect.width - self.rect.width:
            self.x_speed = -self.x_speed
        self.rect.x = self.x
        # 更新boss子弹位置
        now_time = pygame.time.get_ticks()
        if now_time - self.last_shoot_time >= self.shoot_delay:
            self.shoot()
            self.last_shoot_time = now_time

    def shoot(self):
        if self.type == 'alpha':
            new_bullet1 = BossBullet(self.SW_game,self.rect.centerx - 100,self.rect.bottom,self.type)
            new_bullet2 = BossBullet(self.SW_game,self.rect.centerx,self.rect.bottom,self.type)
            new_bullet3 = BossBullet(self.SW_game,self.rect.centerx + 100,self.rect.bottom,self.type)
            self.SW_game.boss_bullets.add(new_bullet1,new_bullet2,new_bullet3)
        elif self.type == 'beta':
            shootx_points = random.choice([self.rect.centerx - 150,self.rect.centerx - 50,self.rect.centerx + 50,self.rect.centerx + 150])
            bullet_x_speed_list = [-3,-1.5,0,1.5,3] 
            for vx in bullet_x_speed_list:
                new_bullet = BossBullet(self.SW_game,shootx_points,self.rect.bottom,self.type)
                new_bullet.x_speed = vx
                self.SW_game.boss_bullets.add(new_bullet)
        elif self.type == 'gamma':
            bullet_types = random.choice(['random','big','fast'])
            if bullet_types == 'random':
                shootx_points = random.randint(self.rect.left,self.rect.right) 
                for _ in range(5):
                    new_bullet = BossBullet(self.SW_game,shootx_points,self.rect.bottom,self.type)
                    vx = random.randint(-3,3)
                    vy = random.randint(1,3)
                    new_bullet.x_speed = vx
                    new_bullet.y_speed = vy
                    self.SW_game.boss_bullets.add(new_bullet)
            elif bullet_types == 'big':
                new_bullet = BossBullet(self.SW_game,self.rect.centerx,self.rect.bottom,self.type)
                new_bullet.image =  self.settings.boss_gamma_big_bullet_image
                new_bullet.rect = new_bullet.image.get_rect()
                new_bullet.rect.midbottom = (self.rect.centerx,self.rect.bottom)
                new_bullet.y = float(new_bullet.rect.y)
                new_bullet.x = float(new_bullet.rect.x)
                new_bullet.y_speed = self.settings.boss_bullet_y_speed[self.type]*0.5
                new_bullet.x_speed = self.settings.boss_bullet_x_speed[self.type]*0.5
                self.SW_game.boss_bullets.add(new_bullet)
            elif bullet_types == 'fast':
                shootx_points = random.randint(self.rect.left,self.rect.right)
                for _ in range(5):
                    new_bullet = BossBullet(self.SW_game,shootx_points,self.rect.bottom,self.type)
                    new_bullet.x_speed = 0
                    new_bullet.y_speed = self.settings.boss_bullet_y_speed[self.type]*3
                    self.SW_game.boss_bullets.add(new_bullet)