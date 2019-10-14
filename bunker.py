import pygame
from pygame.sprite import Sprite


class BunkerTile(Sprite):
    def __init__(self, ai_settings):
        super(BunkerTile, self).__init__()
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/tile.png')
        self.rect = self.image.get_rect()
        # set initial place
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)  # exact position
