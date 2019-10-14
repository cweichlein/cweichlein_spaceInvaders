import pygame
from settings import Settings  # imports just a specific class from settings file
from ship import Ship  # imports just a specific class from ship file
import game_functions as gf  # imports entire game_functions file and assigns it alias "gf"
from pygame.sprite import Group
from game_stats import GameStats
import button as butt
from scoreboard import Scoreboard
from random import randrange
# questions: research statements in ship.py and bullet.py and possibly redundant statement in check_play_button() in gf


def run_game():
    # initialize game, create screen object, group of bullets, and group of aliens
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = butt.Button(ai_settings, screen, "Normal")
    mode_button = butt.ModeButton(ai_settings, screen, "Highscores")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    bunkers = Group()
    bonus = Group()
    explosions = Group()
    gf.create_fleet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, explosions)  # fleet
    gf.create_bunkers(ai_settings, bunkers)  # bunkers
    bonus_tic = randrange(0, 1000)
    # Main loop for game
    while True:
        # Listen for user activity, and input all data. gf is a # file alias
        # tic.increment_tic()
        gf.check_events(ai_settings, screen, stats, play_button, mode_button, sb, ship, bullets, aliens, alien_bullets,
                        bunkers, bonus, explosions)
        if stats.game_active:
            # put things in motion
            if bonus_tic > 10500:  # spawn bonus
                gf.create_bonus(ai_settings, screen, stats, sb, bullets, bonus, explosions)
                bonus_tic = randrange(0, 1000)
            bonus_tic += 1
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens, alien_bullets, bunkers,
                              bonus, explosions)
            gf.update_alien_bullets(ai_settings, stats, ship, alien_bullets,
                                    bunkers)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bonus)
            gf.explosion_update(explosions)
        else:
            file = open('scores.txt', 'w')
            check = 0
            while check != 10:
                file.writelines(str(stats.high_score[check]))
                file.writelines('\n')
                check += 1
            file.close()
        gf.update_screen(ai_settings, screen, stats, play_button, mode_button, sb, ship, bullets, aliens, alien_bullets,
                         bunkers, bonus, explosions)


run_game()
