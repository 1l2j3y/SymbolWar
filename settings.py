from pathlib import Path

import pygame

base_path = Path(__file__).parent
file_path = base_path/'images.py'

class Settings:

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (255,255,255)

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
        self.difficulty_up_delay= 20000

        # Images settings
        self.plane_font = pygame.font.SysFont(None,100)
        self.plane_blink_font = pygame.font.SysFont(None,60)
        self.small_plane_font = pygame.font.SysFont(None,60)
        self.bullet_font = pygame.font.SysFont(None,60)
        self.boss_bullet_font = pygame.font.SysFont(None,100)
        self.boss_gamma_big_bullet_font = pygame.font.SysFont(None,200)
                           
        self.plane_image_str = '(^)'
        self.plane_blink_image_str = '(x_x)'
        self.bullet_image_str = '!'
        self.boss_bullet_image_str = 'o'
        self.boss_gamma_big_bullet_image_str = 'vvv'
        
        self.plane_image = self.plane_font.render(self.plane_image_str,True,self.plane_color)
        self.plane_blink_image = self.plane_blink_font.render(self.plane_blink_image_str,True,self.plane_blink_color)
        self.small_plane_image = self.small_plane_font.render(self.plane_image_str,True,self.small_plane_color)
        self.bullet_image =  self.bullet_font.render(self.bullet_image_str,True,self.bullet_color)
        self.boss_bullet_image = self.boss_bullet_font.render(self.boss_bullet_image_str,True,self.boss_bullet_color)
        self.boss_gamma_big_bullet_image = self.boss_gamma_big_bullet_font.render(self.boss_gamma_big_bullet_image_str,True,self.boss_bullet_color)