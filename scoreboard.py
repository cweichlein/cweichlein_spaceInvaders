import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:

    def __init__(self, ai_settings, screen, stats):
        self.chain_of_high_scores = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (200, 200, 200)
        self.high_score_screen_color = (0, 0, 0)
        self.high_score_screen_color2 = (100, 100, 100)
        self.font = pygame.font.SysFont(None, 48)

        self.score_image = self.font.render('.', True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()

        self.prep_score()
        # self.prep_high_score()

        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()

        self.prep_level()
        # self.prep_ships()
        self.high_score_screen_rect = pygame.Rect(0, 0, self.ai_settings.screen_width,
                                                  self.screen_rect.centery + (self.screen_rect.centery / 2))
        self.main_menu_rect = pygame.Rect(0, 0, self.ai_settings.screen_width, self.ai_settings.screen_height)
        self.msg_score = self.font.render('Best 10', True, self.text_color, self.high_score_screen_color)
        self.msg_score_rect = self.msg_score.get_rect()
        self.msg_score_rect.centerx = self.screen_rect.centerx
        self.msg_score_rect.centery = self.msg_score_rect.height
        self.menu_image = pygame.image.load('images/menu.png')

        self.high_scores_rect = pygame.Rect(self.screen_rect.centerx, self.msg_score_rect.bottom, 64, 64)
        self.msg_high_scores = self.font.render(str(stats.high_score[0]),
                                                True, self.text_color, self.high_score_screen_color)
        ch = 0
        while ch != 10:
            self.chain_of_high_scores[ch] = HighScore(screen, stats, self.text_color, self.high_score_screen_color, ch)
            ch += 1

        self.high_score_image = self.font.render('.', True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()

        self.prep_high_score()

        self.ships = Group()

        self.prep_ships()

    # prep_score and prep_high_score called before show_score, as their rectangles might need to be resized due to
    # an increase in the number (like growing an extra digit)

    def prep_score(self):
        rounded_score = int(round(self.stats.score, 10))
        score_str = "{:,}".format(rounded_score)  # output 1,000,000 instead of 1000000. A "string formatting directive"
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20  # 20 pixels down from top of screen

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score[0], -1))
        high_score_str = "{:,}".format(high_score)  # output 1,000,000 instead of 1000000.
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        for sx in self.chain_of_high_scores:
            sx.update()

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def display_high_scores(self):
        self.screen.fill(self.high_score_screen_color, self.high_score_screen_rect)
        self.screen.blit(self.msg_score, self.msg_score_rect)
        for x in self.chain_of_high_scores:
            x.high_score_draw()

    def display_main_menu(self):
        self.screen.fill(self.high_score_screen_color, self.main_menu_rect)
        self.screen.blit(self.menu_image, self.high_score_screen_rect)


class HighScore:
    def __init__(self, screen, stats, text_color, bg_color, i):
        self.screen = screen
        self.stats = stats
        self.text_color = text_color
        self.bg_color = bg_color
        self.i = i
        self.font = pygame.font.SysFont(None, 28)
        self.screen_rect = screen.get_rect()
        self.high_scores_rect = pygame.Rect(self.screen_rect.centerx, 96 + (32 * i), 64, 64)
        self.msg_high_scores = self.font.render(str(stats.high_score[i]),
                                                True, text_color, bg_color)

    def high_score_draw(self):
        self.screen.fill(self.bg_color, self.high_scores_rect)
        self.screen.blit(self.msg_high_scores, self.high_scores_rect)

    def update(self):
        self.msg_high_scores = self.font.render(str(self.stats.high_score[self.i]),
                                                True, self.text_color, self.bg_color)
