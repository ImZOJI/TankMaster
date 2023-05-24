import pygame as pg
from random import*

class cible:
    def __init__(self, fenx):
        self.proportion = fenx / 1080

        # choix au hasard des coordonées du bonus
        self.x = uniform(100 * self.proportion, 980 * self.proportion)
        self.y = uniform(350 * self.proportion, 450 * self.proportion)
        self.size = 32 * self.proportion
        self.image = pg.transform.scale(pg.image.load("cible-de-flechettes.png"), (self.size, self.size))
        self.hitbox = (self.x, self.y, self.x + self.size, self.y + self.size)
        self.image = pg.transform.scale(self.image, (self.size, self.size))
