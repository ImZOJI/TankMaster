import pygame as pg

class menu:
    def __init__(self, screen):
        self.frq = 60
        self.clock = pg.time.Clock()
        self.time = 0
        self.partie = True
        self.screen = [self.fenx, self.feny] = screen
        self.fond = pg.transform.scale(pg.image.load("fond_menu.png"), (self.fenx, self.feny)).convert()

