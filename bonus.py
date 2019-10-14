import pygame
import math
from pygame.sprite import Sprite
import explosion as exp
import random


class Bonus(Sprite):  # Witch: Flyby bonus

    def __init__(self, ai_settings, screen, stats, sb, bullets, explosions):
        super(Bonus, self).__init__()
        self.stats = stats
        self.sb = sb
        self.bullets = bullets
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/alien_4.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)  # exact position
        self.points = random.randrange(200, 400)
        self.reset = False
        self.explosions = explosions

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * 2)
        self.rect.x = math.floor(self.x)
        self.screen.blit(self.image, self.rect)  # switch to other image
        if self.x >= (self.screen.get_rect()).width:
            self.reset = True
            del self

    def __del__(self):
        if not self.reset:
            self.stats.score += self.points
            new_explosion = exp.Explosion2(self.screen, self.rect.x, self.rect.y, self.points)
            self.explosions.add(new_explosion)
            self.sb.prep_score()
