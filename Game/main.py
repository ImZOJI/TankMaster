from fonctions import *
from bonus import*
from game import*
import sys


pg.init()

pg.mixer.music.load("music.mp3")
pg.mixer.music.play(-1)

game = game()

tank1 = tank("tank1.png", 1, game.fenx, game.feny)
tank2: tank = tank("tank2.png", 2, game.fenx, game.feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

while game.partie:

    game.clock.tick(game.frq)
    game.fen.blit(game.fond, (0, 0))

    game.partie = getevents(joueurs, sys, game.time)

    # Ajout de bonus à intervalle aléatoire

    if game.time - game.tb >= game.cd and len(game.bonus) <= 5:
        game.bonus.append(Bonus(game.fenx))
        cd = uniform(7 * game.frq, 14 * game.frq)
        tb = game.time

    for indice in range(2):
        t = joueurs[indice]
        indiceOp = (indice + 1) % 2
        adv = joueurs[indiceOp]
        tir = True

        t.shield = game.time - t.t_shield <= 5 * game.frq


        for b in t.balle:
            if not b.tir:

                # On dit qu'au moins une balle n'est pas tirée

                tir = False

                # On met à jour la position de la balle et son angle de tir si elle n'est pas tirée

                maj_balle(t, b, game.screen, indice)

            # Dans le cas où la balle est tirée

            else:
                # On met à jour sa position en fonction de la trajectoire de tir

                tir_balle(b, game.time, game.fen)

            # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

            touche_ennemi(b, adv)

            # On vérifie si la balle touche un bonus

            touche_bonus(b, t, adv, game)

        if game.time - t.freezeT > 3 * 60 or t.shield:
            t.freeze = False

        if not tir:
            # On affiche la trajectoire de tir

            traj(t, t.balle[-1], game.fen)

        move(t, game.fen, tir)

        t.affiche_vie(game.fen)

    # Affiche les bonus disponibles.
    for bon in game.bonus:
        game.fen.blit(bon.image, [bon.x, bon.y])

    pg.display.update()
    game.time += 1
