from tkinter import SW

from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self,SW_game,direction=1):
        super().__init__()
            #  获取游戏屏幕对象和设置对象
        self.screen = SW_game.screen
        self.screen_rect = SW_game.screen_rect
        self.settings = SW_game.settings
        self.color = self.settings.bullet_color
            # 创建一个表示子弹的矩形,并设置其初始位置
        self.image = self.settings.bullet_image
        self.rect = self.image.get_rect()
        self.y = float(self.rect.y)
        self.direction = direction
        # 更新子弹位置
    def updata(self):
        self.y -= self.settings.bullet_speed * self.direction
        if self.rect.bottom < self.screen_rect.top and self.rect.top > self.screen_rect.bottom:
            self.kill()
        self.rect.y = self.y

class BossBullet(Sprite):

    def __init__(self,SW_game,x,y,boss_type):
        super().__init__()
            #  获取游戏屏幕对象和设置对象
        self.screen = SW_game.screen
        self.screen_rect = SW_game.screen_rect
        self.settings = SW_game.settings
        self.color = self.settings.boss_bullet_color
            # 创建一个表示子弹的矩形,并设置其初始位置
        self.image = self.settings.boss_bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.y_speed = self.settings.boss_bullet_y_speed[boss_type]
        self.x_speed = self.settings.boss_bullet_x_speed[boss_type]

        # 更新子弹位置
    def update(self):
        self.y += self.y_speed
        self.x += self.x_speed
        if self.rect.top > self.screen_rect.bottom:
            self.kill()
        else:
            self.rect.y = self.y
            self.rect.x = self.x