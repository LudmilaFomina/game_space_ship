import pygame as pg
from game_settings import SCORE


class Score(pg.sprite.Sprite):
    """to keep track of the score."""

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.font = pg.font.Font(None, 30)
        self.font.set_italic(0)
        self.color = "white"
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 10)

    def update(self):
        """We only update the score in update() when it has changed."""
        if SCORE.value != self.lastscore:
            self.lastscore = SCORE.value
            msg = f"Score: {SCORE.value}"
            self.image = self.font.render(msg, 0, self.color)
