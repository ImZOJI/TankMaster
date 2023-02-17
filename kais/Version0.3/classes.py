import pygame as pg
from math import*

class tank:
    def __init__(self, img: str, j: int, fenx, feny):
        self.propx = fenx / 1080
        self.propy = feny / 675
        print(self.propx, self.propy)
        self.j = j
        self.posx = (10+996*(j-1)) * self.propx
        self.posy = 600 * self.propy
        self.tir = True
        self.size = 64 * self.propx
        self.image = pg.transform.scale(pg.image.load(img), (self.size, self.size))
        self.balle = balle(self.propx, self.propy)
        self.g = False
        self.d = False
        self.plus = False
        self.moins = False
        self.vie = 5
        self.hitbox = (self.posx, self.posy, self.size, self.size)

    def gauche(self):
        if self.j == 1 and self.posx > 10 * self.propx:
            self.posx -= 3 * self.propx
        elif self.j == 2 and self.posx > 550 * self.propx:
            self.posx -= 3 * self.propx

    def droite(self):
        if self.j == 1 and self.posx < 467 * self.propx:
            self.posx += 3
        if self.j == 2 and self.posx < 1006 * self.propx:
            self.posx += 3

    def affiche_vie(self,fen):
        coeur = pg.transform.scale(pg.image.load("coeur.png"), (self.size, self.size)).convert_alpha()
        for i in range(self.vie):
            if self.j == 1:
                fen.blit(coeur.convert_alpha(), ((10 + i* 74) * self.propx, 10 * self.propy))
            else:
                fen.blit(coeur.convert_alpha(), (((1080-10-64) - i* 74) * self.propx, 10 * self.propy))

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
        self.fleche = pg.transform.scale(pg.image.load("fleche.png"), (64 * self.propx, 64 * self.propy))
        self.t0 = 0
        self. pos0 = 0
        self.hitbox = (self.posx, self.posy, self.size, self.size)
        self.v = 750
        self.g = 400
        self.mult = 1

    def affiche(self, fen):

        rotated_image = pg.transform.rotate(self.fleche, self.angle)
        #recentre l'image
        taille = rotated_image.get_size()
        x = self.posx - (taille[0]//2)
        y = self.posy - (taille[1]//2)
        fen.blit(rotated_image, (x, y))

    def angle_plus(self):
        if self.angle < 89:
            self.angle += 1
        elif self.angle > 91:
            self.angle -= 1

    def angle_moins(self):
        if 90 > self.angle > 1:
            self.angle -= 1
        elif 179 > self.angle > 90:
            self.angle += 1

    def shoot(self, t):
        if self.posy < 664 * self.propy:
            self.posx = self.pos0 + (32 + cos(self.angle * pi / 180) * self.v * self.mult*t) * self.propx
            self.posy = (600 + self.g * (self.mult*t) ** 2 - sin(self.angle * pi / 180) * self.v * self.mult*t) * self.propy
        else :
            self.tir = False
