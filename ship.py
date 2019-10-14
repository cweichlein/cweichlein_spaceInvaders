import pygame
from pygame.sprite import Sprite
import math as math


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()  # research this
        self.screen = screen  # save passed screen object as local variable "screen"
        self.ai_settings = ai_settings
        self.sheet = [pygame.image.load('images/ship1_1.png'), pygame.image.load('images/ship1_2.png'),
                      pygame.image.load('images/ship1_3.png'), pygame.image.load('images/ship1_4.png'),
                      pygame.image.load('images/ship1_5.png'), pygame.image.load('images/ship1_6.png'),
                      pygame.image.load('images/ship1_7.png'), pygame.image.load('images/ship1_8.png'),
                      pygame.image.load('images/ship1_9.png')]
        self.cell = 0
        self.image = self.sheet[self.cell]
        self.rect = self.image.get_rect()  # gets the image's rectangle
        self.screen_rect = screen.get_rect()  # gets the passed screen object's rectangle
        # place ships in center and at bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
        self.explode = pygame.mixer.Sound('sounds/alien_alert.wav')
        self.die = False
        self.respawn = False
        self.timer = 0

    # Reads the movement flags and updates the ship's position accordingly
    def update(self):
        if not self.die:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor
            self.rect.centerx = math.floor(self.center)
        else:
            self.timer += 1
            if self.timer > 20:
                self.timer = 0
                self.image = self.sheet[self.cell]
                self.cell += 1
                if self.cell == 9:
                    self.die = False
                    self.cell = 0
                    self.image = self.sheet[0]
                    self.respawn = True
            self.rect.centerx = math.floor(self.center)

    # draws ship image at the current position of self.rect
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
