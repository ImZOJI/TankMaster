import pygame as pg
import sys

def quitter(fen):
    fen.blit(pg.transform.scale(pg.image.load("quitter.png"), (272, 80)).convert(), [268, 320])
    while True:
        evt = pg.event.poll()
        if evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE:
                return True
        elif evt.type == pg.KEYDOWN and evt.key == pg.K_RETURN:
            sys.exit()
            return False