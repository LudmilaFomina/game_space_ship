import pygame as pg
import os


class ScoreValue:
    def __init__(self):
        self.value = 0


# game constants
MAX_SHOTS = 10          # maximum number of player's bullets on screen

ALIEN_ODDS = 5          # chances a new alien appears
ALIEN_RELOAD = 100      # frame before new alien

BOMB_ODDS = 60          # chances a new bomb will drop

GIFT_ODDS = 0.1          # chances a new gift appears (0.0 - 1.0)
GIFT_RELOAD = 200       # frame before new gift

SCREENRECT = pg.Rect(0, 0, 675, 1000)
SCORE = ScoreValue()





MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
