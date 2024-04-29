import pygame as pg
import os


class ScoreValue:
    def __init__(self):
        self.value = 0



# game constants
MAX_SHOTS = 10      # maximum number of player bullets on screen
ALIEN_ODDS = 5      # chances a new alien appears
BOMB_ODDS = 60      # chances a new bomb will drop
ALIEN_RELOAD = 100   # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 675, 1000)
SCORE = ScoreValue()





MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
