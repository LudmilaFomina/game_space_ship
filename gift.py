import pygame as pg
import random
from typing import List
from game_settings import SCREENRECT


class Gift(pg.sprite.Sprite):
    """The gift appears in a random place at the top of the screen
    and gives +10 points to the player
    when it comes into contact with a spaceship"""

    animcycle = 12
    period = 70
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x_vel = random.choice((-1, 1, 0))
        self.y_vel = 2
        self.frame = 0
        self.rect.right = random.uniform(111, SCREENRECT.right)

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)
        if not SCREENRECT.contains(self.rect):
            self.x_vel = -self.x_vel
            self.rect = self.rect.clamp(SCREENRECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]
        if self.frame % self.period == 0:
            self.x_vel = 0
        if self.rect.bottom >= SCREENRECT.height:
            self.kill()