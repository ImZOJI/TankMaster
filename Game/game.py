import pygame as pg


class game:
    def __init__(self):
        self.frq = 60
        self.clock = pg.time.Clock()
        self.time = 0
        self.fen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.partie = True
        self.screen = [self.fenx, self.feny] = self.fen.get_size()
        self.fond = pg.transform.scale(pg.image.load("background.jpeg"), (self.fenx, self.feny)).convert()
        self.bonus = []
        self.cd = 0  # temps avant l'apparition du prochain bonus
        self.tb = 0  # temps à l'apparition du dernier bonus
