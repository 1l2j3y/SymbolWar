from pygame.sprite import Sprite

class Plane(Sprite):

    def __init__(self,PW_game):
        super().__init__()
            # 获取游戏屏幕对象和设置对象
        self.screen = PW_game.screen
        self.settings = PW_game.settings
        self.screen_rect = PW_game.screen.get_rect()
            # 加载飞机图像并获取其外接矩形
        self.image = self.settings.plane_image
        self.rect = self.image.get_rect()
            # 这是将飞机坐标转换为小数，以便更精确地控制飞机的移动
        self.rect.x = float(self.rect.x)
        self.rect.y = float(self.rect.y)
            # 将飞机放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
            #  移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
            # 飞机速度
        self.speed = self.settings.plane_speed
            # 飞机生命值
        self.health = self.settings.plane_health
            # 飞机无敌状态
        self.invincible = False
        self.invincibility_duration = self.settings.plane_invincibility_duration
        # 更新飞机位置
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.speed
        # 绘制飞机
    def plane_draw(self):
        if self.invincible:
            self.image = self.settings.plane_blink_image
        else:
            self.image = self.settings.plane_image
        self.screen.blit(self.image,self.rect)

class SmallPlane(Sprite):

    def __init__(self,PW_game):
        super().__init__()
        
        self.settings = PW_game.settings
            # 加载飞机图像并获取其外接矩形
        self.image = self.settings.small_plane_image
        self.rect = self.image.get_rect()