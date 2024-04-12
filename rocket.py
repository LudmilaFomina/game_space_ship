import pygame as pg
from typing import List

from blast import Blast
from explosion import Explosion
from game_settings import SCORE


class Rocket(pg.sprite.Sprite):
    """a rocket the Player sprite fires."""
    speed = -11
    images: List[pg.Surface] = []

    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def explode(self):
        return Blast(self.rect.center, self.groups())

    def update(self):
        """called every time around the game loop.
        Every tick we move the shot upwards.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()
