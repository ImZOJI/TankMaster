import pygame as pg

class fin:
    def __init__(self):
        self.frq = 60
        self.clock = pg.time.Clock()
        self.time = 0
        self.fen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.partie = False
        self.screen = [self.fenx, self.feny] = self.fen.get_size()
        self.fond = pg.transform.scale(pg.image.load("background.png"), (self.fenx, self.feny)).convert()

