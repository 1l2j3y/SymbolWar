import pygame.font

class Button:

    def __init__(self, SW_game,msg,y_add=0):
        self.screen = SW_game.screen
        self.settings = SW_game.settings
        self.screen_rect = self.screen.get_rect()
            # 按钮属性
        self.button_color = self.settings.button_color
        self.text_color = self.settings.text_color
        self.button_width = self.settings.button_width
        self.button_height = self.settings.button_height
        self.font = pygame.font.SysFont(None, 48)
            # 创建按钮的rect对象,并设置其位置
        self.rect = pygame.Rect(0, 0, self.button_width,self.button_height)
        self.rect.center = self.screen_rect.center
        self.rect.centery += y_add

        self.button_text_draw(msg)

        # 将文本图片绘制在按钮上
    def button_text_draw(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
        # 绘制按钮
    def button_draw(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)