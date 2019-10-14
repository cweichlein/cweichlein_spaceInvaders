import pygame
from pygame.sprite import Sprite
import random


class AlienBullet(Sprite):
    def __init__(self, ai_settings, screen, alien):
        super(AlienBullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        ai_settings.bullet_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
