from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self,PW_game):
        super().__init__()
            #  获取游戏屏幕对象和设置对象
        self.screen = PW_game.screen
        self.settings = PW_game.settings
        self.color = self.settings.bullet_color
            # 创建一个表示子弹的矩形,并设置其初始位置
        self.image = self.settings.bullet_image
        self.rect = self.image.get_rect()
        self.rect.midtop = PW_game.plane.rect.midtop
        self.y = float(self.rect.y)
        # 更新子弹位置
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y