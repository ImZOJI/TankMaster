import pygame as pg
from math import*

class tank:
    def __init__(self, img: str, j: int):
        self.j = j
        self.posx = 10 + 996*(j-1)
        self.posy = 600
        self.tir = True
        self.size = 64
        self.image = pg.image.load(img).convert_alpha()
        self.balle = balle()
        self.g = False
        self.d = False
        self.plus = False
        self.moins = False
        self.vie = 5
        self.hitbox = (self.posx, self.posy, self.size, self.size)

    def gauche(self):
        if self.j == 1 and self.posx > 10:
            self.posx -= 1
        elif self.j == 2 and self.posx > 550:
            self. posx -= 1

    def droite(self):
        if self.j == 1 and self.posx < 467:
            self.posx += 1
        if self.j == 2 and self.posx < 1006:
            self.posx += 1

class balle:
    def __init__(self):
        self.posx = 0
        self.posy = 0 #600
        self.angle = 44
        self.tir = False
        self.size = 16
        self.image = pg.image.load("balle.png").convert_alpha()
        self.fleche = pg.image.load("fleche.png")
        self.t0 = 0
        self. pos0 = 0
        self.hitbox = (self.posx, self.posy, self.size, self.size)

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
        if self.posy < 700 :
            self.posx = self.pos0 + cos(self.angle * pi / 180) * 1500 * t
            self.posy = 600 + 400 * t ** 2 - sin(self.angle * pi / 180) * 500 * t
        else :
            self.tir = False
