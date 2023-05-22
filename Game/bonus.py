import pygame as pg
from random import*

class Bonus:
    def __init__(self, fen):
        self.proportion = fen / 1080

        # choix au hasard des coordonées du bonus
        self.x = uniform(100 * self.proportion, 980 * self.proportion)
        self.y = uniform(350 * self.proportion, 450 * self.proportion)

        self.types = ["freeze", "ball", "tank_speed", "ball_speed", "shield"]
        self.type = randint(0, len(self.types) - 1)                     # choix au hasard du type de bonus
        img = self.types[self.type] + ".png"                            # affecte la bonne image en fonction du type
        self.image = pg.image.load(img)
        self.size = 32*self.proportion
        self.hitbox = (self.x, self.y, self.x + self.size, self.y + self.size)
        self.image = pg.transform.scale(self.image, (self.size, self.size))
