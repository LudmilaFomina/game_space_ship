#!/usr/bin/env python
"""
Controls:
--------
'Left' and 'right' arrows to move
'Space bar' to shoot
'n' key for rocket
'm' key for rocket explosion
'l' key for laser
'f' key to toggle between fullscreen
"""

import os
import pygame as pg
import random
import argparse

from alien import Alien
from blast import Blast
from bomb import Bomb
from explosion import Explosion
from player import Player
from rocket import Rocket
from score import Score
from shot import Shot
from laser import Laser
from gift import Gift
from tools import load_image, load_sound
from game_settings import (MAX_SHOTS, ALIEN_ODDS, BOMB_ODDS, GIFT_ODDS, ALIEN_RELOAD,
                           GIFT_RELOAD, SCREENRECT, SCORE, MAIN_DIR)


# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


class Game:

    def __init__(self):
        self.winstyle = 0
        self.fullscreen = False
        self.screen = None
        self.bestdepth = None
        self.alienreload = ALIEN_RELOAD
        self.giftreload = GIFT_RELOAD

    ########################################
    # public interfaces
    ########################################
    def initialize(self, no_sound):
        # Initialize pygame
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()

        self._init_sound(no_sound)
        self._init_display()
        self._load_images()
        self._load_sounds()
        self._init_groups()

        self.clock = pg.time.Clock()

    def play(self):
        while self.player.alive():
            self._process_events()

            # clear/erase the last drawn sprites
            self._all.clear(self.screen, self.background)
            # update all the sprites
            self._all.update()

            # handle player input
            keystate = pg.key.get_pressed()

            self._input_move_player(keystate)
            self._input_fire_bullet(keystate)
            self._input_fire_rocket(keystate)
            self._input_explode_rocket(keystate)
            self._input_fire_laser(keystate)

            self._create_new_alien()
            self._alien_drop_bombs()
            self._create_new_gift()

            self._check_alien_player_collision()
            self._check_bomb_player_collision()
            self._check_gift_player_collision()

            self._check_bullets_aliens_collision()
            self._check_rocket_aliens_collision()
            self._check_laser_aliens_collision()

            # draw the scene
            dirty = self._all.draw(self.screen)
            pg.display.update(dirty)

            # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
            self.clock.tick(40)

    def close(self):
        if pg.mixer:
            pg.mixer.music.fadeout(1000)
        pg.time.wait(1000)
    ########################################
    # private interfaces
    ########################################
    ########################################
    # initialization
    ########################################

    def _init_sound(self, no_sound):
        if no_sound:
            pg.mixer = None
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None

    def _init_display(self):
        self.bestdepth = pg.display.mode_ok(
            SCREENRECT.size,
            self.winstyle,
            32)
        self.screen = pg.display.set_mode(
            SCREENRECT.size,
            self.winstyle,
            self.bestdepth)

    def _load_images(self):
        # Load images, assign to sprite classes
        img = load_image('spaceship.gif')
        Player.images = [img, pg.transform.flip(img, 1, 0)]
        img = load_image("explo.gif")
        Explosion.orig_images = [img, pg.transform.flip(img, 1, 0)]
        Alien.images = [load_image(im) for im in ("ali1.gif", "ali2.gif", "ali3.gif")]
        Bomb.images = [load_image("bomb.gif")]
        Shot.images = [load_image("shot.gif")]
        Rocket.images = [load_image("rocket.gif")]
        Laser.images = [load_image("lazer.gif")]
        Gift.images = [load_image(im) for im in ("cow1.gif", "cow2.gif", "cow3.gif")]

        # decorate the game window
        icon = pg.transform.scale(Alien.images[0], (32, 32))
        pg.display.set_icon(icon)
        pg.display.set_caption("Pygame Aliens")
        pg.mouse.set_visible(0)

        # create the background, tile the bgd image
        bgdtile = load_image("fonn.jpg")
        self.background = pg.Surface(SCREENRECT.size)
        for x in range(0, SCREENRECT.width, bgdtile.get_width()):
            self.background.blit(bgdtile, (x, 0))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()

    def _load_sounds(self):
        # load the sound effects
        self.boom_sound = load_sound("boom.wav")
        self.shoot_sound = load_sound("car_door.wav")
        self.rocket_sound = load_sound("rocket.mp3")
        self.laser_sound = load_sound("laser.mp3")
        self.gift_sound = load_sound("moo.mp3")
        if pg.mixer:
            music = os.path.join(MAIN_DIR, "data", "tango.mp3")
            # Musical composition: Tango-La Cumparsita-Rodríguez-Arranged for Strings
            pg.mixer.music.load(music)
            pg.mixer.music.play(-1)
            self.boom_sound.set_volume(0.5)
            self.laser_sound.set_volume(0.4)

    def _init_groups(self):
        # Initialize Game Groups
        self.aliens = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.gifts = pg.sprite.Group()
        self._all = pg.sprite.RenderUpdates()
        self.lastalien = pg.sprite.GroupSingle()
        # instance for a rocket and laser
        self.rocket = None
        self.laser = None
        self.player = Player(self._all)
        Alien(
            self.aliens, self._all, self.lastalien
        )  # note, this 'lives' because it goes into a sprite group
        if pg.font:
            self._all.add(Score(self._all))

    ########################################
    # game loop
    ########################################
    def _process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not self.fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = self.screen.copy()
                        self.screen = pg.display.set_mode(
                            SCREENRECT.size,
                            self.winstyle | pg.FULLSCREEN,
                            self.bestdepth
                        )
                        self.screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = self.screen.copy()
                        self.screen = pg.display.set_mode(
                            SCREENRECT.size,
                            self.winstyle,
                            self.bestdepth
                        )
                        self.screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    self.fullscreen = not self.fullscreen

    def _input_move_player(self, keystate):
        direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        self.player.move(direction)

    def _input_fire_bullet(self, keystate):
        firing = keystate[pg.K_SPACE]
        if (
                not self.player.reloading
                and firing 
                and len(self.shots) < MAX_SHOTS):
            Shot(self.player.gunpos(), self.shots, self._all)
            self._play_shoot_sound()
        self.player.reloading = firing

    def _input_fire_rocket(self, keystate):
        rocketing = keystate[pg.K_n]
        if not self.player.reloading_rocket and rocketing and self.rocket == None:
            self.rocket = Rocket(self.player.gunpos(), self._all)
            self._play_rocket_sound()
        self.player.reloading_rocket = rocketing

    def _input_explode_rocket(self, keystate):
        rocket_exploding = keystate[pg.K_m]
        if rocket_exploding and self.rocket:
            self._explode_rocket()
            self.rocket = None

    def _explode_rocket(self):
        blast = self.rocket.explode()
        for alien in pg.sprite.spritecollide(
                blast, self.aliens, 1):
            self._explode(alien)
            SCORE.value += 1
        self._explode(blast)
        self.rocket.kill()
        blast.kill()

    def _input_fire_laser(self, keystate):
        lasering = keystate[pg.K_l]
        if not self.player.reloading_laser and lasering and self.laser == None:
            self.laser = Laser(self.player.gunpos(), self._all)
            self._play_laser_sound()
        self.player.reloading_laser = lasering

    def _explode_laser(self):
        blast = self.laser.explode()
        for alien in pg.sprite.spritecollide(
                blast, self.aliens, 1):
            self._explode(alien)
            SCORE.value += 1
        self._explode(blast)
        self.laser.kill()
        blast.kill()

    def _create_new_alien(self):
        # Create new alien
        if self.alienreload:
            self.alienreload = self.alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien(self.aliens, self._all, self.lastalien)
            self.alienreload = ALIEN_RELOAD

    def _alien_drop_bombs(self):
        # Drop bombs
        if self.lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(self.lastalien.sprite, self._all, self.bombs, self._all)

    def _create_new_gift(self):
        if self.giftreload != 0:
            self.giftreload = self.giftreload - 1
        else:
            if random.random() <= GIFT_ODDS:
                Gift(self.gifts, self._all)
                self.giftreload = GIFT_RELOAD

    def _check_alien_player_collision(self):
        # Detect collisions between aliens and players.
        for alien in pg.sprite.spritecollide(self.player, self.aliens, 1):
            self._play_boom_sound()
            self._explode(alien)
            self._explode(self.player)
            SCORE.value += 1
            self.player.kill()

    def _check_bullets_aliens_collision(self):
        # See if shots hit the aliens.
        for alien in pg.sprite.groupcollide(self.aliens, self.shots, 1, 1).keys():
            self._play_boom_sound()
            self._explode(alien)
            SCORE.value += 1

    def _check_rocket_aliens_collision(self):
        # See if rockets hit the aliens.
        if self.rocket:
            rocket_collision = False
            for alien in pg.sprite.spritecollide(self.rocket, self.aliens, 1):
                self._play_boom_sound()
                self._explode(alien)
                SCORE.value += 1
                rocket_collision = True
            if rocket_collision:
                self._explode_rocket()
                self.rocket = None

    def _check_laser_aliens_collision(self):
        # See if laser hit the aliens.
        if self.laser:
            for alien in pg.sprite.spritecollide(self.laser, self.aliens, 1):
                self._play_boom_sound()
                self._explode(alien)
                SCORE.value += 1
            if self.laser.laser_duration_counter == Laser.laser_duration:
                self.laser.kill()
                self.laser = None

    def _check_bomb_player_collision(self):
        # See if alien bombs hit the player.
        for bomb in pg.sprite.spritecollide(self.player, self.bombs, 1):
            self._play_boom_sound()
            self._explode(self.player)
            self._explode(bomb)
            self.player.kill()

    def _check_gift_player_collision(self):
        # Detect collisions between gift and player
        for gift in pg.sprite.spritecollide(self.player, self.gifts, 1):
            #self._play_boom_sound()
            SCORE.value += 10
            self._play_gift_sound()

    def _play_boom_sound(self):
        if pg.mixer and self.boom_sound is not None:
            self.boom_sound.play()

    def _play_shoot_sound(self):
        if pg.mixer and self.shoot_sound is not None:
            self.shoot_sound.play()

    def _play_rocket_sound(self):
        if pg.mixer and self.rocket_sound is not None:
            self.rocket_sound.play()

    def _play_laser_sound(self):
        if pg.mixer and self.laser_sound is not None:
            self.laser_sound.play()

    def _play_gift_sound(self):
        if pg.mixer and self.gift_sound is not None:
            self.gift_sound.play()

    def _explode(self, obj):
        Explosion(obj, self._all)


def main():
    parser = argparse.ArgumentParser(description='Control commands:')
    parser.add_argument('-s', action='store_true', help='Sound off')
    args = parser.parse_args()
    print('Sound:', args.s)

    game = Game()
    game.initialize(args.s)
    game.play()
    game.close()


if __name__ == "__main__":
    main()
    pg.quit()
