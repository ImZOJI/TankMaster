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
        self.tempsInitial = 0                                   # temps auquel la balle a été tiré
        self.positionInitiale = 0                               # position initiale du tir
        self.hitbox = (self.posx, self.posy, self.size, self.size)
        self.vitesse = 750
        self.gravité = 400
        self.multiplicateur = 1
        self.gel = False

    def affiche(self, fen):

        for pt in range(8) :
            x = self.positionInitiale + (cos(self.angle * pi / 180) * self.vitesse * pt / 50) * self.propx
            y = (520 + self.gravité * (pt / 50) ** 2 - sin(self.angle * pi / 180) * self.vitesse * pt / 50) \
                * self.propy
            fen.blit(self.point, (x, y))

    def shoot(self, time):
        t = (time - self.tempsInitial) / 60
        if self.posy < 664 * self.propy:
            self.posx = self.positionInitiale + (cos(self.angle * pi / 180) * self.vitesse * self.multiplicateur * t) * self.propx
            self.posy = (520 + self.gravité * (self.multiplicateur * t) ** 2 - sin(self.angle * pi / 180) * self.vitesse * self.multiplicateur * t) * \
                        self.propy
        else :
            self.tir = False
