from pygame.sprite import Group

from plane import SmallPlane

class Gui:

    def __init__(self,PW_game):
        self.PW_game = PW_game
        self.screen = PW_game.screen
        self.screen_rect = PW_game.screen.get_rect()
        self.settings = PW_game.settings
        self.stats = PW_game.stats

        self.text_color = self.settings.GUI_text_color
        self.font = self.settings.GUI_font

        self.score_GUI_create()
        self.image_GUI_create()
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
    def image_GUI_create(self):
            # 剩余血量
        self.small_planes = Group()
        for plane_num in range(self.stats.plane.health):
            small_plane = SmallPlane(self.PW_game)
            small_plane.rect.left = plane_num*small_plane.rect.width
            small_plane.rect.top = 0
            self.small_planes.add(small_plane)
        # 绘制GUI
    def draw(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.difficulty_image,self.difficulty_rect)
        self.small_planes.draw(self.screen)