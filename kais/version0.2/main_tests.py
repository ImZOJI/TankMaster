from classes import *
from fonctions import *
import time

pg.init()

partie = True
fen = pg.display.set_mode((1080, 720))
fond = pg.image.load("background.png").convert()

tank1 = tank("tank1.png", 1)
tank2 = tank("tank2.png", 2)
joueurs = [tank1, tank2]
joueurs[1].balle.angle = 136
frequency = 60
F = True
ti = time.time()
font = pg.font.SysFont('arial', 24)
while partie:
    if F:
        ti = time.time()
        dt = 1/frequency
        F = False
    else:
        dt = time.time() - ti
        if dt >= 1/frequency:
            F = True
            fen.blit(fond, [0, 0])
            text = font.render(str(1 / dt), True, (0, 255, 0))
            fen.blit(text, (500,10))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            patrie = False
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                partie = False
                sys.exit()
            if event.key == pg.K_q:
                joueurs[0].g = True
            if event.key == pg.K_d:
                joueurs[0].d = True
            if event.key == pg.K_z:
                joueurs[0].plus = True
            if event.key == pg.K_s:
                joueurs[0].moins = True
            if event.key == pg.K_RIGHT:
                joueurs[1].d = True
            if event.key == pg.K_LEFT:
                joueurs[1].g = True
            if event.key == pg.K_UP:
                joueurs[1].plus = True
            if event.key == pg.K_DOWN:
                joueurs[1].moins = True
            if event.key == pg.K_SPACE:
                if not joueurs[0].balle.tir:
                    joueurs[0].balle.t0 = time.time()
                    joueurs[0].balle.pos0 = joueurs[0].posx
                joueurs[0].balle.tir = True
            if event.key == pg.K_RETURN:
                if not joueurs[1].balle.tir:
                    joueurs[1].balle.t0 = time.time()
                    joueurs[1].balle.pos0 = joueurs[1].posx
                joueurs[1].balle.tir = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                joueurs[0].g = False
            if event.key == pg.K_d:
                joueurs[0].d = False
            if event.key == pg.K_z:
                joueurs[0].plus = False
            if event.key == pg.K_s:
                joueurs[0].moins = False
            if event.key == pg.K_RIGHT:
                joueurs[1].d = False
            if event.key == pg.K_LEFT:
                joueurs[1].g = False
            if event.key == pg.K_UP:
                joueurs[1].plus = False
            if event.key == pg.K_DOWN:
                joueurs[1].moins = False
    for indice in range(2):
        t = joueurs[indice]
        indiceOp = (indice + 1) % 2
        adv = joueurs[indiceOp]
        if not t.balle.tir:
            if F:
                if t.g:
                    t.gauche()
                if t.d:
                        t.droite()
                if t.plus:
                    t.balle.angle_plus()
                if t.moins:
                    t.balle.angle_moins()
                t.hitbox = (t.posx, t.posy, t.size, t.size)
        else:
            t.balle.shoot(time.time() - t.balle.t0)
            t.balle.hitbox = (t.balle.posx, t.balle.posy, t.balle.size, t.balle.size)
            if F:
                fen.blit(t.balle.image, (t.balle.posx, t.balle.posy))
        if F:
            fen.blit(t.image, [t.posx, t.posy])
            t.affiche_vie(fen)
            if not t.balle.tir:
                t.balle.affiche(fen)
        if not t.balle.tir:
            t.balle.posx = t.posx + (55 * ((indice + 1) % 2))
            t.balle.posy = t.posy + 10
        if adv.hitbox[0] < t.balle.posx < adv.hitbox[0] + adv.hitbox[2] and adv.hitbox[1] < t.balle.posy < \
                adv.hitbox[1] + adv.hitbox[3]:
            t.balle.tir = False
            adv.vie -= 1
    if F:
        pg.display.update()
pg.quit()
