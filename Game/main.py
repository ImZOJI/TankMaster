from fonctions import *
from bonus import*
from game import*
import sys


pg.init()

pg.mixer.music.load("music.mp3")
pg.mixer.music.play(-1)

game = game()

tank1 = tank("tank1.png", 1, game.fenx, game.feny)
tank2 = tank("tank2.png", 2, game.fenx, game.feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

while game.partie:

    game.clock.tick(game.frq)
    game.fen.blit(game.fond, (0, 0))

    game.partie = getevents(joueurs, sys, game.time)

    # Ajout de bonus à intervalle aléatoire

    if game.time - game.lastBonusTime >= game.couldown and len(game.bonus) <= 5:
        game.bonus.append(Bonus(game.fenx))
        cooldown = uniform(7 * game.frq, 14 * game.frq)
        lastBonusTime = game.time

    for indice in range(2):
        tank = joueurs[indice]
        indiceAdversaire = (indice + 1) % 2
        adv = joueurs[indiceAdversaire]
        tir = True

        tank.shield = game.time - tank.t_shield <= 5 * game.frq


        for ball in tank.balle:
            if not ball.tir:

                # On dit qu'au moins une balle n'est pas tirée

                tir = False

                # On met à jour la position de la balle et son angle de tir si elle n'est pas tirée

                maj_balle(tank, ball, game.screen, indice)

            # Dans le cas où la balle est tirée

            else:
                # On met à jour sa position en fonction de la trajectoire de tir

                tir_balle(ball, game.time, game.fen)

            # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

            touche_ennemi(ball, adv)

            # On vérifie si la balle touche un bonus

            touche_bonus(ball, tank, adv, game)

        if game.time - tank.freezeT > 3 * 60 or tank.shield:
            tank.freeze = False

        if not tir:
            # On affiche la trajectoire de tir

            dessineTrajectoire(tank, tank.balle[-1], game.fen)

        deplace(tank, game.fen, tir)

        tank.affiche_vie(game.fen)

    # Affiche les bonus disponibles.
    for bon in game.bonus:
        game.fen.blit(bon.image, [bon.x, bon.y])

    pg.display.update()
    game.time += 1
