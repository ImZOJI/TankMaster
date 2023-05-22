from fonctions import *
from bonus import*
from game import*
from modesolo import*
from menu import*
from fin import*
import sys


pg.init()

pg.mixer.music.load("music.mp3")
pg.mixer.music.play(-1)

fen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

mainMenu(fen)