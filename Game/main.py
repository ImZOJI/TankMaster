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
screen = [fenx, feny] = fen.get_size()

game = game(screen)
modesolo = modesolo(screen)
menu = menu(screen)
fin = fin(screen)

tank1 = tank("tank1.png", 1, game.fenx, game.feny)
tank2 = tank("tank2.png", 2, game.fenx, game.feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

#mode solo
tankSolo = tank("tank1.png", 1, modesolo.fenx, modesolo.feny)
joueurSolo =[tankSolo]
joueurSolo[0].angle = 136

jeu = True

while jeu:

    mainMenu(fen, screen)

    while game.partie:



        game.clock.tick(game.frq)
        fen.blit(game.fond, (0, 0))

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

                tir_balle(ball, game.time, fen)

            # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

            touche_ennemi(ball, adv)

            # On vérifie si la balle touche un bonus

            touche_bonus(ball, tank, adv, game)

        if game.time - tank.freezeT > 3 * 60 or tank.shield:
            tank.freeze = False

        if not tir:
            # On affiche la trajectoire de tir

            dessineTrajectoire(tank, tank.balle[-1], fen)

        deplace(tank, fen, tir)

        tank.affiche_vie(fen)

        # Affiche les bonus disponibles.
        for bon in game.bonus:
            fen.blit(bon.image, [bon.x, bon.y])

        if joueurs[0].vie == 0 or joueurs[1].vie == 0 :
            game.partie = False
            fin.partie = True

        pg.display.update()
        game.time += 1

    partieSolo(fen)

    while fin.partie:

        joueurs[0].vie = 5
        joueurs[0].propx = game.fenx / 1080
        joueurs[0].posx = (10+996*(1-1)) * joueurs[0].propx
        joueurs[1].vie = 5
        joueurs[1].propx = game.fenx / 1080
        joueurs[1].posx = (10 + 996 * (2 - 1)) * joueurs[1].propx
        game.time = 0
        game.bonus = []
        game.cd = 0  # temps avant l'apparition du prochain bonus
        game.tb = 0  # temps à l'apparition du dernier bonus


        couleur = (255, 255, 255)

        couleur_sombre = (36, 63, 93)
        couleur_claire = (61, 72, 77)

        smallfont = pg.font.SysFont('Cooper', 35)
        fond = pg.transform.scale(pg.image.load("fond_menu.png"), (fin.fenx, fin.feny)).convert()
        quit = smallfont.render('QUITTER', True, couleur)
        goMenu = smallfont.render('MENU', True, couleur)


        while fin.partie:
            fen.blit(fond, [0, 0])
            for ev in pg.event.get():

                if ev.type == pg.QUIT:
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:

                    if (fin.fenx / 2.2 <= mouse[0] <= fin.fenx / 2.2 + 140) and (
                            fin.feny / 1.5 <= mouse[1] <= fin.feny / 1.5 + 40):
                        sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    if (fin.fenx / 2.2 <= mouse[0] <= fin.fenx / 2.2 + 140) and (
                            fin.feny / 3 <= mouse[1] <= fin.feny / 3 + 40):
                        menu.partie = True
                        fin.partie = False

            # coordonnes de la souris dans un tuple
            mouse = pg.mouse.get_pos()

            # quand la souris passe sur le bouton la couleur change
            if (fin.fenx / 2.2 <= mouse[0] <= fin.fenx / 2.2 + 140) and (fin.feny / 3 <= mouse[1] <= fin.feny / 3 + 40):
                pg.draw.rect(fen, couleur_sombre, [fin.fenx / 2.2, fin.feny / 3, 140, 40])

            else:
                pg.draw.rect(fen, couleur_claire, [fin.fenx / 2.2, fin.feny / 3, 140, 40])
            fen.blit(goMenu, (fin.fenx / 2.2 + 28, fin.feny / 3 + 10))

            if (fin.fenx / 2.2 <= mouse[0] <= fin.fenx / 2.2 + 140) and (fin.feny / 1.5 <= mouse[1] <= fin.feny / 1.5 + 40):
                pg.draw.rect(fen, couleur_sombre, [fin.fenx / 2.2, fin.feny / 1.5, 140, 40])



            else:
                pg.draw.rect(fen, couleur_claire, [fin.fenx / 2.2, fin.feny / 1.5, 140, 40])

                # superimposing the text onto our button
            fen.blit(quit, (fin.fenx / 2.2 + 14, fin.feny / 1.5 + 10))

            # updates the frames of the game
            pg.display.update()