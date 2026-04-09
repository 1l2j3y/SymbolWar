import random

from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self,PW_game):
        super().__init__()
            # 获取游戏屏幕对象和设置对象
        self.screen = PW_game.screen
        self.settings = PW_game.settings
        self.screen_rect = PW_game.screen.get_rect()
            # 加载敌机图像并获取其外接矩形
        self.image = self.settings.enemy_image
        self.rect = self.image.get_rect()
            # 这是将敌机坐标转换为小数，以便更精确地控制敌机的移动
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
            # 敌机速度
        self.y_speed = self.settings.enemy_y_speed
        self.x_speed = random.choice([-self.settings.enemy_x_speed, self.settings.enemy_x_speed])

        self.enemy_spawn_delay = PW_game.stats.enemy_spawn_delay
        # 更新敌机位置
    def update(self):
        self.y += self.y_speed
        self.rect.y = self.y
        self.x += self.x_speed
        if self.x < 0 or self.x > self.screen_rect.width - self.rect.width:
            self.x_speed = -self.x_speed
        self.rect.x = self.x
        # 增加敌人速度
    def speedup(self,difficulty=0):
        self.y_speed += self.settings.enemy_y_speed_up*difficulty
        self.x_speed += self.settings.enemy_x_speed_up*difficulty