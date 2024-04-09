import pygame as pg


class Blast(pg.sprite.Sprite):
    """describes a blast from rocket"""

    width = 400
    height = 400

    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.Surface([self.width, self.height])
        self.rect = self.image.get_rect(center=pos)
