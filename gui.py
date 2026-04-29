import pygame
from pygame.sprite import Group

from plane import SmallPlane

class Gui:

    def __init__(self,SW_game):
        self.SW_game = SW_game
        self.screen = SW_game.screen
        self.screen_rect = SW_game.screen.get_rect()
        self.settings = SW_game.settings
        self.stats = SW_game.stats

        self.text_color = self.settings.GUI_text_color
        self.font = self.settings.GUI_font

        self.score_GUI_create()
        self.plane1_health_GUI_create(self.SW_game.plane1)
        self.plane2_health_GUI_create(self.SW_game.plane2,50)
        self.difficulty_GUI_create()
        # 创建字符串GUI的图像并设置他们的位置
    def score_GUI_create(self):
            # 得分
        self.score_str = str(f'score: {self.stats.score:,}')
        self.score_image = self.font.render(self.score_str,True,self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 0
            # 最高得分
        self.highest_score_str = str(f'highest score: {self.stats.highest_score:,}')
        self.highest_score_image = self.font.render(self.highest_score_str,True,self.text_color)
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.right = self.screen_rect.right - 20
        self.highest_score_rect.top = 80
            # 难度
    def difficulty_GUI_create(self):
        self.difficulty_str = str(f'difficulty: {self.stats.difficulty:,}')
        self.difficulty_image = self.font.render(self.difficulty_str,True,self.text_color)
        self.difficulty_rect = self.difficulty_image.get_rect()
        self.difficulty_rect.right = self.screen_rect.right - 20
        self.difficulty_rect.top = 40

        # 创建图片GUI的图像并设置他们的位置
    def plane_health_GUI_create(self,plane,top=0):
            # 剩余血量
        if plane.id == 1:
            self.small_planes1 = Group()
        else:
            self.small_planes2 = Group()
        for plane_num in range(plane.health):
            small_plane = SmallPlane(self.SW_game)
            small_plane.rect.left = plane_num*small_plane.rect.width
            small_plane.rect.top = top
            if plane.id == 1:
                self.small_planes1.add(small_plane)
            else:
                self.small_planes2.add(small_plane)

        # boss血条创建(含boss名字)
    def boss_health_GUI_create(self,boss):
        if boss is None:
            return
        health_bar_rect = pygame.Rect(0,0,700,30)
        health_bar_rect.centerx = self.screen_rect.centerx
        health_bar_rect.top = 10
        pygame.draw.rect(self.screen,self.settings.boss_health_bar_color,health_bar_rect)
        rest_health_rect_width = int(health_bar_rect.width*(boss.health/self.settings.boss_health[boss.type]))
        rest_health_rect = pygame.Rect(0,0,rest_health_rect_width,30)
        rest_health_rect.left = health_bar_rect.left
        rest_health_rect.top = health_bar_rect.top
        pygame.draw.rect(self.screen,self.settings.boss_rest_health_bar_color,rest_health_rect)
        boss_name_str = boss.type.title()
        boss_name_image = self.font.render(boss_name_str,True,self.settings.boss_color)
        boss_name_rect = boss_name_image.get_rect()
        boss_name_rect.centerx = self.screen_rect.centerx
        boss_name_rect.top = health_bar_rect.bottom + 10
        self.screen.blit(boss_name_image,boss_name_rect)

        # 绘制GUI
    def draw(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.difficulty_image,self.difficulty_rect)
        self.small_planes1.draw(self.screen)