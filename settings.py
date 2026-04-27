from pathlib import Path
import json

import pygame

base_path = Path(__file__).parent

class Settings:

    def __init__(self):
        # Background settings
        self.bg_image = pygame.image.load(base_path / 'assets' / 'bg.png').convert()
        self.bg_y1 = 0
        self.bg_y2 = None
        self.bg_scroll_speed = 0.3
        self.bg_color = (255,255,255)

        # Backgroundmusic settings
        self.bgm_path = base_path / 'assets' / 'bgm.ogg'
        self.boss_bgm_path = base_path / 'assets' / 'boss_bgm.ogg'
        self.bgm_volume = 0.2

        # Sound settings
        self.shoot_sound = pygame.mixer.Sound(base_path / 'assets' / 'shoot.wav')
        self.shoot_sound.set_volume(0.1)
        self.enemy_killed_sound = pygame.mixer.Sound(base_path / 'assets' / 'enemy_killed.wav')
        self.enemy_killed_sound.set_volume(0.3)
        self.boss_killed_sound = pygame.mixer.Sound(base_path / 'assets' / 'boss_killed.wav')
        self.boss_killed_sound.set_volume(1)
        self.plane_hit_sound = pygame.mixer.Sound(base_path / 'assets' / 'plane_hit.wav')
        self.plane_hit_sound.set_volume(0.5)
        self.game_over_sound = pygame.mixer.Sound(base_path / 'assets' / 'game_over.wav')
        self.game_over_sound.set_volume(1)
        self.translate_sound = pygame.mixer.Sound(base_path / 'assets' / 'translate.wav')
        self.translate_sound.set_volume(1)

        # Plane settings
        self.plane_speed = 2
        self.plane_health = 3
        self.plane_blink_time = 200
        self.plane_invincibility_duration = 2000
        self.plane_color = (0,0,0)
        self.small_plane_color = (0,0,0)
        self.plane_blink_color = (255,0,0)
        
        # Bullet settings
        self.bullet_speed = 2
        self.max_bullets = 5
        self.bullet_color = (0,0,0)
        self.boss_bullet_y_speed = {'alpha':2,'beta':1.5,'gamma':1.5}
        self.boss_bullet_x_speed = {'alpha':0,'beta':1.5,'gamma':2}
        self.boss_bullet_image = None
        self.boss_bullet_color = (255,0,0)
        
        # Enemy settings
        self.max_enemies = 10
        self.enemy_spawn_delay = 1000
        self.enemy_color = (200,0,0)
        self.enemy_health = {'dive':1,'sweep':1,'tank':3}
        self.enemy_y_speed = {'dive':1,'sweep':0.5,'tank':0.3}
        self.enemy_x_speed = {'dive':0,'sweep':1,'tank':0.3}

        ## Boss settings
        self.boss_health = {'alpha':100,'beta':200,'gamma':300}
        self.boss_y_speed = {'alpha':0,'beta':0,'gamma':0}
        self.boss_x_speed = {'alpha':0.5,'beta':0,'gamma':0.3}
        self.boss_shoot_delay = {'alpha':1500,'beta':1000,'gamma':2000}
        self.boss_color = (200,0,0)
        self.boss_health_bar_color = (255,0,0)
        self.boss_rest_health_bar_color = (0,255,0)

        # Button settings
        self.button_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.button_width = 200
        self.button_height = 50

        # GUI settings
        self.GUI_text_color = (30,30,30)
        self.GUI_font = pygame.font.SysFont(None,48)

        # score settings
        self.enemy_points = {'dive':10,'sweep':20,'tank':30}
        self.boss_points = 1000

        # Difficulty settings
        self.enemy_x_speed_up = 0.1
        self.enemy_y_speed_up = 0.1
        self.enemy_maxnum_up = 1
        self.enemy_spawn_delay_down_coefficient = 0.9
        self.enemy_spawn_min_delay = 200
        self.difficulty_up_delay= 30000

        # Help settings
        self.help_text_en = [
            'Use arrow keys to move the plane.',
            'Press space to shoot.',
            'Destroy enemies to earn points.',
            'Difficulty increases every 30 seconds.',
            'Bosses will appear at higher difficulties and high scores.',
            'Good luck and have fun!',
            'Press Esc to exit the game.',
            'Click anywhere to close this help window.',
            '本帮助界面没有汉化,请不要输入114514并回车']
        self.help_text_ch = ["你终究还是输入了这串恶臭的数字",
                            "方向键移动, 空格键开火, ESC退出",
                            "半分钟加一次难度",
                            " boss会在分数和时间都达到的时候出现",
                            "这就是全部内容了",
                            "建议不要外放,音效比较抽象"]
        
        self.help_window_size = (650, 350)
        self.help_bg_color = (255, 255, 255)
        self.help_text_color = (0, 0, 0)
        self.help_text_font = pygame.font.SysFont('SimHei', 20)
        self.help_title_font = pygame.font.SysFont(None, 40)
        
        self.help_text_lines = self.help_text_en
        self.help_window = pygame.Surface(self.help_window_size)
        self.help_window.fill(self.help_bg_color)
        self.help_window_rect = self.help_window.get_rect()

        # Images settings
        self.plane_font = pygame.font.SysFont(None,100)
        self.plane_blink_font = pygame.font.SysFont(None,60)
        self.small_plane_font = pygame.font.SysFont(None,60)
        self.bullet_font = pygame.font.SysFont(None,60)
        self.boss_bullet_font = pygame.font.SysFont(None,100)
        self.boss_gamma_big_bullet_font = pygame.font.SysFont(None,200)
                           
        self.plane_image_str = '/(^)\\'
        self.plane_blink_image_str = '(x_x)'
        self.bullet_image_str = '!'
        self.boss_bullet_image_str = 'o'
        self.boss_gamma_big_bullet_image_str = 'OOO'

        self.help_text_title_str = 'Welcome to Symbol War !'

        self.plane_image = self.plane_font.render(self.plane_image_str,True,self.plane_color)
        self.plane_blink_image = self.plane_blink_font.render(self.plane_blink_image_str,True,self.plane_blink_color)
        self.small_plane_image = self.small_plane_font.render(self.plane_image_str,True,self.small_plane_color)
        self.bullet_image =  self.bullet_font.render(self.bullet_image_str,True,self.bullet_color)
        self.boss_bullet_image = self.boss_bullet_font.render(self.boss_bullet_image_str,True,self.boss_bullet_color)
        self.boss_gamma_big_bullet_image = self.boss_gamma_big_bullet_font.render(self.boss_gamma_big_bullet_image_str,
                                                                                  True,self.boss_bullet_color)
        
        self.help_text_title_image = self.help_title_font.render(self.help_text_title_str,True,self.help_text_color)
        self.help_text_title_rect = self.help_text_title_image.get_rect()

        # Language settings
        self.language = 'en'

    def zoom_bg_image(self,screen_rect):
        self.bg_image = pygame.transform.smoothscale(self.bg_image,(screen_rect.width,screen_rect.height))
        self.bg_y2 = -screen_rect.height