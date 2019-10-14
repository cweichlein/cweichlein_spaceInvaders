import os.path
import pygame


class GameStats:
    def __init__(self, ai_settings):
        self.score = 0
        self.level = 1
        self.broke_high_score = False
        self.ai_settings = ai_settings
        self.ships_left = self.ai_settings.ship_limit
        self.reset_stats()
        # Start game in an inactive state.
        self.game_active = False
        self.music_tracks = [pygame.mixer.Sound('sounds/alien_bg.wav'), pygame.mixer.Sound('sounds/alien_bg2.wav'),
                             pygame.mixer.Sound('sounds/alien_bg3.wav'), pygame.mixer.Sound('sounds/alien_bg4.wav')]
        self.music_phase = 0
        self.current = self.music_tracks[0]
        self.music_check = 0

        self.high_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # read into array from score.txt
        if not os.path.exists('scores.txt'):
            file = open('scores.txt', 'w+')
            k = 0
            while k < 9:
                file.write(str(0))
                file.write("\n")
                k += 1
            file.write(str(0))
        else:
            file = open('scores.txt')
        x = 0
        for read_in in file:
            if read_in.strip():
                self.high_score[x] = int(read_in)
                x += 1
        file.close()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.broke_high_score = False
        self.music_phase = 0

    def start_music(self, check):
        if check != self.music_check:
            self.music_check = check
            self.current.stop()
            if self.music_phase < 4:
                self.music_phase += 1
            self.current = pygame.mixer.Sound(self.music_tracks[self.music_phase])
            self.current.play()

    def music_reset(self):
        self.music_phase = -1
        self.start_music(100)

    def music_stop(self):
        self.current.stop()
