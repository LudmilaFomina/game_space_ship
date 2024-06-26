import pygame as pg
from typing import List


class Explosion(pg.sprite.Sprite):
    """Alien's explosion"""
    defaultlife = 12
    animcycle = 3
    orig_images: List[pg.Surface] = []

    def __init__(self, actor, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.images = self.scale_by_actor(
            actor.rect.center,
            actor.rect.width,
            self.orig_images)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def scale_by_actor(self, center_coor, actor_width, orig_imgs):
        imgs = []
        for i in range(len(orig_imgs)):
            rect = orig_imgs[i].get_rect(center=center_coor)
            imgs.append(
                pg.transform.scale_by(
                    orig_imgs[i], (actor_width / rect.width)))
        return imgs

    def update(self):
        """Called every time around the game loop.
        Shows the explosion surface for 'default life'.
        Every game tick(update), we decrease the 'life'.
        Also we animate the explosion
        """
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()
