from pathlib import Path

import pygame

base_path = Path(__file__).parent
file_path = base_path/'images.py'

class Settings:

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        # Plane settings
        self.plane_speed = 2
        self.plane_health = 3
        self.plane_blink_time = 200
        self.plane_invincibility_duration = 2000
        self.plane_color = (0,0,0)
        
        # Bullet settings
        self.bullet_speed = 1
        self.max_bullets = 5
        self.bullet_color = (0,0,0)
        
        # Enemy settings
        self.enemy_y_speed = 0.2
        self.enemy_x_speed = 0.7
        self.max_enemies = 10
        self.enemy_spawn_delay = 1000
        self.enemy_color = (0,0,0)
        
        # Button settings
        self.button_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.button_width = 200
        self.button_height = 50
        # GUI settings
        self.GUI_text_color = (30,30,30)
        self.GUI_font = pygame.font.SysFont(None,48)
        # score settings
        self.enemy_points = 10
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
        self.enemy_font = pygame.font.SysFont(None,80)
        self.plane_image_str = '(^)'
        self.plane_blink_image_str = '(x_x)'
        self.bullet_image_str = '!'
        self.enemy_image_str = 'v'
        self.plane_image = self.plane_font.render(self.plane_image_str,True,self.plane_color)
        self.plane_blink_image = self.plane_blink_font.render(self.plane_blink_image_str,True,self.plane_color)
        self.small_plane_image = self.small_plane_font.render(self.plane_image_str,True,self.plane_color)
        self.bullet_image =  self.bullet_font.render(self.bullet_image_str,True,self.bullet_color)
        self.enemy_image = self.enemy_font.render(self.enemy_image_str,True,self.enemy_color)