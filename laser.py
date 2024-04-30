import pygame as pg
from typing import List
from blast import Blast


class Laser(pg.sprite.Sprite):
    """a laser the Player sprite fires."""
    laser_duration = 40
    images: List[pg.Surface] = []

    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.laser_duration_counter = 0

    def explode(self):
        return Blast(self.rect.center, self.groups())

    def update(self):
        """called every time around the game loop.
        Every tick we move the laser upwards.
        """
        self.laser_duration_counter += 1
