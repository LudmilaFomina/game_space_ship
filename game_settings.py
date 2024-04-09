import pygame as pg
import os

# game constants
MAX_SHOTS = 10  # most player bullets onscreen
ALIEN_ODDS = 5  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 30  # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 960, 640)
SCORE = 0

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
