import pygame
from pygame.sprite import Sprite
import math
import random
import alien_bullet
import explosion


class Alien(Sprite):
    def __init__(self, ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions):
        super(Alien, self).__init__()
        self.sb = sb
        self.explosions = explosions
        self.alter_move = alter_move
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        # load image and set rect
        self.sheet = [pygame.image.load('images/alien1_1.png'), pygame.image.load('images/alien1_1.png')]
        self.image = self.sheet[0]
        self.rect = self.image.get_rect()
        self.tic = 0
        self.gun_tic = 0
        self.alien_bullets = alien_bullets

        # set initial place
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)  # exact position
        self.explode = pygame.mixer.Sound('sounds/alien_alienHit.wav')
        self.shiftDown = pygame.mixer.Sound('sounds/alien_downRow.wav')

        self.random_gun_tic = random.randint(1000, 10000)
        self.can_fire = False
        self.reset = False

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.shiftDown.play()
            return True
        elif self.rect.left <= 0:
            self.shiftDown.play()
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = math.floor(self.x)
        self.tic += 1
        self.gun_tic += 1
        if self.tic <= self.ai_settings.alien_jitter_speed:
            self.screen.blit(self.sheet[0], self.rect)  # switch to other image
            self.image = self.sheet[0]
        elif self.tic <= (2 * self.ai_settings.alien_jitter_speed):
            self.screen.blit(self.sheet[1], self.rect)  # switch to other image
            self.image = self.sheet[1]
            if self.tic >= (2 * self.ai_settings.alien_jitter_speed):
                self.tic = 0
        if self.can_fire:
            if self.gun_tic >= (1 * self.random_gun_tic):
                new_alien_bullet = alien_bullet.AlienBullet(self.ai_settings, self.screen, self)
                self.alien_bullets.add(new_alien_bullet)
                self.gun_tic = 0


class Alien1(Alien):  # Laughing pumpkins: weak
    def __init__(self, ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions):
        super(Alien1, self).__init__(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
        if alter_move:
            self.sheet = [pygame.image.load('images/alien1_1.png'), pygame.image.load('images/alien1_2.png')]
            self.image = self.sheet[0]
        else:
            self.sheet = [pygame.image.load('images/alien1_2.png'), pygame.image.load('images/alien1_1.png')]
            self.image = self.sheet[0]

    def __del__(self):  # destructor: Automatically called when instance is deleted
        if not self.reset:
            self.explode.play()
            self.stats.score += 10
            new_explosion = explosion.Explosion(self.screen, self.rect.x, self.rect.y)
            self.explosions.add(new_explosion)
            self.sb.prep_score()


class Alien2(Alien):  # Bleeding ghosts: Vomits at the wizard upon death.
    def __init__(self, ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions):
        super(Alien2, self).__init__(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
        self.sheet = [pygame.image.load('images/alien2_1.png'), pygame.image.load('images/alien2_2.png')]
        self.image = self.sheet[0]

    def __del__(self):  # This modified destructor will unleash a wave of three bullets upon activation
        if not self.reset:
            self.explode.play()
            self.stats.score += 20
            new_explosion = explosion.Explosion(self.screen, self.rect.x, self.rect.y)
            self.explosions.add(new_explosion)
            self.sb.prep_score()
            new_alien_bullet1 = alien_bullet.AlienBullet(self.ai_settings, self.screen, self)
            new_alien_bullet2 = alien_bullet.AlienBullet(self.ai_settings, self.screen, self)
            new_alien_bullet2.rect.centerx -= self.rect.width
            new_alien_bullet3 = alien_bullet.AlienBullet(self.ai_settings, self.screen, self)
            new_alien_bullet3.rect.centerx += self.rect.width
            self.alien_bullets.add(new_alien_bullet1)
            self.alien_bullets.add(new_alien_bullet2)
            self.alien_bullets.add(new_alien_bullet3)


class Alien3(Alien):  # Undead Cowboys: Fire candles at player periodically
    def __init__(self, ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions):
        super(Alien3, self).__init__(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
        self.sheet = [pygame.image.load('images/alien3_1.png'), pygame.image.load('images/alien3_2.png')]
        self.image = self.sheet[0]
        self.can_fire = True

    def __del__(self):  # destructor: Automatically called when instance is deleted
        if not self.reset:
            self.explode.play()
            self.stats.score += 30
            new_explosion = explosion.Explosion(self.screen, self.rect.x, self.rect.y)
            self.explosions.add(new_explosion)
            self.sb.prep_score()
