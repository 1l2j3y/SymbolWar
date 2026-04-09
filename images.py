import pygame

class Image:

    def __init__(self):
        self.plane_str = '@'
        

    def score_GUI_create(self):
            # 得分
        self.score_image = self.font.render(self.score_str,True,self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 0