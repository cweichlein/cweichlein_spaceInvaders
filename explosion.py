import pygame
from pygame.sprite import Sprite
import pygame.font


class Explosion(Sprite):
    def __init__(self, screen, x, y):
        super(Explosion, self).__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.sheet = [pygame.image.load('images/explosion_1.png'),
                      pygame.image.load('images/explosion_2.png'),
                      pygame.image.load('images/explosion_3.png')]
        self.rect = self.sheet[0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.slide = 0
        self.image = self.sheet[self.slide]
        self.tic = 0

    def update(self):
        self.screen.blit(self.sheet[self.slide], self.rect)  # switch to other image
        self.image = self.sheet[self.slide]
        if self.tic > 25:
            self.tic = 0
            if self.slide >= 2:
                self.kill()
            else:
                self.slide += 1
        else:
            self.tic += 1


class Explosion2(Explosion):
    def __init__(self, screen, x, y, points):
        super(Explosion2, self).__init__(screen, x, y)
        self.text_color = (200, 200, 200)
        self.font = pygame.font.SysFont(None, 24)
        self.screen_color = (0, 0, 0)
        self.msg_score = self.font.render(str(points), True, self.text_color, self.screen_color)
        self.msg_score_rect = self.msg_score.get_rect()
        self.msg_score_rect.centerx = x
        self.msg_score_rect.centery = y
        self.image = self.msg_score

    def update(self):
        self.screen.blit(self.msg_score, self.msg_score_rect)
        self.tic += 1
        if self.tic > 85:
            self.kill()
