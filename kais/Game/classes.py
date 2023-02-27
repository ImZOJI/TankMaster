import pygame as pg
from math import*
from random import*

class tank:
    def __init__(self, img: str, j: int, fenx, feny):
        self.propx = fenx / 1080
        self.propy = feny / 675
        print(self.propx, self.propy)
        self.j = j
        self.posx = (10+996*(j-1)) * self.propx
        self.posy = 600 * self.propy
        self.size = 64 * self.propx
        self.image = pg.transform.scale(pg.image.load(img), (self.size, self.size))
        self.balle = [balle(self.propx, self.propy)]
        self.g = False
        self.d = False
        self.plus = False
        self.moins = False
        self.vie = 5
        self.hitbox = (self.posx, self.posy, self.size, self.size)
        self.angle = self.balle[0].angle

        # Attributs pour application de bonus


        self.freeze_img = pg.transform.scale(pg.image.load(img[:5] + "_gel.png"), (self.size, self.size))
        self.freeze = False
        self.freezeT = 0
        self.vit = 3
        self.t_shield = 0
        self.shield = False
        self.shield_img = pg.transform.scale(pg.image.load(img[:5] + "_shield.png"), (self.size, self.size))

    def gauche(self):
        if self.j == 1 and self.posx > 10 * self.propx:
            self.posx -= self.vit * self.propx
        elif self.j == 2 and self.posx > 550 * self.propx:
            self.posx -= self.vit * self.propx

    def droite(self):
        if self.j == 1 and self.posx < 467 * self.propx:
            self.posx += self.vit * self.propx
        if self.j == 2 and self.posx < 1006 * self.propx:
            self.posx += self.vit * self.propx

    def affiche_vie(self,fen):
        coeur = pg.transform.scale(pg.image.load("coeur.png"), (self.size, self.size)).convert_alpha()
        for i in range(self.vie):
            if self.j == 1:
                fen.blit(coeur.convert_alpha(), ((10 + i* 74) * self.propx, 10 * self.propy))
            else:
                fen.blit(coeur.convert_alpha(), (((1080-10-64) - i* 74) * self.propx, 10 * self.propy))

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
        self.gel = False

    def affiche(self, fen):

        rotated_image = pg.transform.rotate(self.fleche, self.angle)
        # recentre l'image
        taille = rotated_image.get_size()
        x = self.posx - (taille[0]//2)
        y = self.posy - (taille[1]//2)
        fen.blit(rotated_image, (x, y))


    def shoot(self, t):
        if self.posy < 664 * self.propy:
            self.posx = self.pos0 + (32 + cos(self.angle * pi / 180) * self.v * self.mult*t) * self.propx
            self.posy = (600 + self.g * (self.mult*t) ** 2 - sin(self.angle * pi / 180) * self.v * self.mult*t)\
                        * self.propy
        else:
            self.tir = False


class Bonus:
    def __init__(self, fen):
        self.prop = fen/1080
        self.x = uniform(100*self.prop, 980*self.prop)
        self.y = uniform(350*self.prop, 450*self.prop)
        self.types = ["freeze", "ball", "speed", "ball_s", "shield"]
        self.type = randint(0, len(self.types) - 1)
        img = self.types[self.type] + ".png"
        self.image = pg.image.load(img)
        '''
        match self.type:
            case 0:
                self.image = pg.image.load("freeze.png")
            case 1:
                self.image = pg.image.load("ball.png")
            case 2:
                self.image = pg.image.load("speed.png")
            case 3:
                self.image = pg.image.load("ball_s.png")
            case 4:
                self.image = pg.image.load("shield.png")
            case _:
                self.image = None
        '''
        self.size = 32*self.prop
        self.hitbox = (self.x, self.y, self.x + self.size, self.y + self.size)
        self.image = pg.transform.scale(self.image, (self.size, self.size))
