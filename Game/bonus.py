import pygame as pg
from random import*

class Bonus:
    def __init__(self, fen):
        self.prop = fen/1080
        self.x = uniform(100*self.prop, 980*self.prop)
        self.y = uniform(350*self.prop, 450*self.prop)
        self.types = ["freeze", "ball", "speed", "ball_s", "shield"]
        self.type = randint(0, len(self.types) - 1)
        img = self.types[self.type] + ".png"
        self.image = pg.image.load(img)
        self.size = 32*self.prop
        self.hitbox = (self.x, self.y, self.x + self.size, self.y + self.size)
        self.image = pg.transform.scale(self.image, (self.size, self.size))
