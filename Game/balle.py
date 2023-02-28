import pygame as pg
from math import *


class balle:
    def __init__(self, propx, propy):
        self.propx = propx
        self.propy = propy
        self.posx = 0
        self.posy = 600
        self.angle = 44
        self.tir = False
        self.size = 16 * self.propx
        self.image = pg.transform.scale(pg.image.load("balle.png"), (self.size, self.size)).convert_alpha()
        self.point = pg.transform.scale(pg.image.load("traj.png"), (8 * self.propx, 8 * self.propy))
        self.t0 = 0
        self.pos0 = 0
        self.hitbox = (self.posx, self.posy, self.size, self.size)
        self.v = 750
        self.g = 400
        self.mult = 1
        self.gel = False

    def affiche(self, fen):

        for pt in range(8) :
            x = self.pos0 + (cos(self.angle * pi / 180) * self.v * pt / 50) * self.propx
            y = (520 + self.g * (pt / 50) ** 2 - sin(self.angle * pi / 180) * self.v * pt / 50) \
                * self.propy
            fen.blit(self.point, (x, y))

    def shoot(self, time):
        t = (time - self.t0) / 60
        if self.posy < 664 * self.propy:
            self.posx = self.pos0 + (cos(self.angle * pi / 180) * self.v * self.mult * t) * self.propx
            self.posy = (520 + self.g * (self.mult * t) ** 2 - sin(self.angle * pi / 180) * self.v * self.mult * t) * \
                        self.propy
        else :
            self.tir = False
