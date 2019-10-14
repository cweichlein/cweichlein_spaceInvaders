import pygame


class Settings:
    def __init__(self):
        self.alien_jitter_speed = 60
        self.mode = -1
        self.bullet_color = 10, 10, 200
        self.alien_points = 0
        # screen settings
        # self.screen_width = 900
        self.screen_width = 450
        # self.screen_height = 600
        self.screen_height = 600
        # self.bg_color = (230, 230, 230)
        self.bg_color = (0, 0, 0)
        self.ship_speed_factor = 0.2
        self.bullet_speed_factor = 1.5
        self.alien_bullet_speed_factor = 0.4
        self.bullet_width = 5
        self.bullet_height = 15
        # self.bullet_color = 10, 10, 200
        self.bullets_allowed = 1
        # self.alien_speed_factor = 1
        self.alien_speed_factor = 0.1
        self.fleet_drop_speed = 10  # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.ship_limit = 3
        self.speedup_scale = 1.1  # will be applied to all objects in the game
        self.score_scale = 1.5  # rate score increases per bullet-alien hit with each stage
        self.initialize_dynamic_settings()
        self.levelUp = pygame.mixer.Sound('sounds/alien_stageUp.wav')
        self.gameOver = pygame.mixer.Sound('sounds/alien_gameOver.wav')
        self.brokeHighScore = pygame.mixer.Sound('sounds/alien_highScore.wav')

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 0.2
        self.bullet_speed_factor = 1.5
        # self.alien_speed_factor = 1
        self.alien_speed_factor = 0.1
        self.fleet_direction = 1
        self.alien_points = 50  # initialized here because it grows with stage increase
        self.alien_jitter_speed = 60
        self.mode = -1
        self.bullet_color = 10, 10, 200

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # self.alien_jitter_speed -= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)  # comment out when not testing
