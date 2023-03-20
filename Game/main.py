from fonctions import *
from bonus import*
import sys


pg.init()

frq = 60
clock = pg.time.Clock()
time = 0

partie = True
fen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
'''fen = pg.display.set_mode((1080, 675))'''
screen = [fenx, feny] = fen.get_size()

fond = pg.transform.scale(pg.image.load("background.jpeg"), (fenx, feny)).convert()

tank1 = tank("tank1.png", 1, fenx, feny)
tank2: tank = tank("tank2.png", 2, fenx, feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

bonus = []
cd = 0  # temps avant l'apparition du prochain bonus
tb = 0  # temps à l'apparition du dernier bonus

font = pg.font.SysFont('arial', 24)

while partie:

    clock.tick(frq)
    fen.blit(fond, (0, 0))

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
                if not joueurs[0].freeze:
                    for b in joueurs[0].balle:
                        if not b.tir:
                            b.t0 = time
                            b.tir = True
                            break
            if event.key == pg.K_RETURN:
                if not joueurs[1].freeze:
                    for b in joueurs[1].balle:
                        if not b.tir:
                            b.t0 = time
                            b.pos0 = joueurs[1].posx
                            b.tir = True
                            break
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

    # Ajout de bonus à intervalle aléatoire

    if time - tb >= cd and len(bonus) <= 5:
        bonus.append(Bonus(fenx))
        cd = uniform(7 * frq, 14 * frq)
        tb = time

    for indice in range(2):
        t = joueurs[indice]
        indiceOp = (indice + 1) % 2
        adv = joueurs[indiceOp]
        tir = True

        t.shield = time - t.t_shield <= 5 * frq

        for b in t.balle:
            if not b.tir:

                # On dit qu'au moins une balle n'est pas tirée

                tir = False

                # On met à jour la position de la balle et son angle de tir si elle n'est pas tirée

                maj_balle(t, b, screen, indice)

                # On affiche la trajectoire de tir

                traj(t, b, fen)

            # Dans le cas où la balle est tirée

            else:
                # On met à jour sa position en fonction de la trajectoire de tir

                tir_balle(b, time, fen)

            # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

            touche_ennemi(b, adv)

            # On vérifie si la balle touche un bonus

            touche_bonus(b, t, adv, bonus, time)

        if time - t.freezeT > 3 * 60 or t.shield:
            t.freeze = False

        move(t, fen, tir)

        t.affiche_vie(fen)

    # Affiche les bonus disponibles.
    for bon in bonus:
        fen.blit(bon.image, [bon.x, bon.y])

    pg.display.update()
    time += 1
