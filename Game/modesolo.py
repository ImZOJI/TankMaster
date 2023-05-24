import pygame as pg

class modesolo:
    def __init__(self, screen):
        self.frq = 60
        self.clock = pg.time.Clock()
        self.time = 0
        self.partie = False
        self.screen = [self.fenx, self.feny] = screen
        self.fond = pg.transform.scale(pg.image.load("background.jpeg"), (self.fenx, self.feny)).convert()
        self.score = 0