from fonctions import *
from bonus import*
from game import*
from modesolo import*
from menu import*
from fin import*
import sys


pg.init()

game = game()
modesolo = modesolo()
menu = menu()
fin = fin()

tank1 = tank("tank1.png", 1, game.fenx, game.feny)
tank2: tank = tank("tank2.png", 2, game.fenx, game.feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

#mode solo
tankSolo = tank("tank1.png", 1, modesolo.fenx, modesolo.feny)
joueurs2 =[tankSolo]
joueurs2[0].angle = 136

jeu = True

while jeu:

    while menu.partie:

        res = (menu.fenx, menu.feny)

        screen = pg.display.set_mode(res)

        couleur = (255, 255, 255)

        couleur_sombre = (36, 63, 93)
        couleur_claire = (61, 72, 77)
        longueur = screen.get_width()
        hauteur = screen.get_height()

        smallfont = pg.font.SysFont('Cooper', 35)
        fond = pg.transform.scale(pg.image.load("fond_menu.png"), (menu.fenx, menu.feny)).convert()
        quit = smallfont.render('QUITTER', True, couleur)
        jouer = smallfont.render('MULTI 2J', True, couleur)
        solo = smallfont.render('SOLO', True, couleur)
        while menu.partie:
            screen.blit(fond, [0, 0])
            for ev in pg.event.get():

                if ev.type == pg.QUIT:
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:

                    if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (
                            hauteur / 1.5 <= mouse[1] <= hauteur / 1.5 + 40):
                        sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (
                            hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                        game.partie = True
                        menu.partie = False

                if ev.type == pg.MOUSEBUTTONDOWN:
                    if (longueur / 2.2  + 150<= mouse[0] <= longueur / 2.2 + 290) and (
                            hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                        modesolo.partie = True
                        menu.partie = False

            # coordonnes de la souris dans un tuple
            mouse = pg.mouse.get_pos()

            # quand la souris passe sur le bouton la couleur change
            if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                pg.draw.rect(screen, couleur_sombre, [longueur / 2.2, hauteur / 3, 140, 40])

            else:
                pg.draw.rect(screen, couleur_claire, [longueur / 2.2, hauteur / 3, 140, 40])
            screen.blit(jouer, (longueur / 2.2 + 18, hauteur / 3 + 10))

            if (longueur / 2.2 + 150 <= mouse[0] <= longueur / 2.2 + 290) and (hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                pg.draw.rect(screen, couleur_sombre, [longueur / 2.2 + 150, hauteur / 3, 140, 40])

            else:
                pg.draw.rect(screen, couleur_claire, [longueur / 2.2 + 150, hauteur / 3, 140, 40])
            screen.blit(solo, (longueur / 2.2 + 178, hauteur / 3 + 10))

            if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (hauteur / 1.5 <= mouse[1] <= hauteur / 1.5 + 40):
                pg.draw.rect(screen, couleur_sombre, [longueur / 2.2, hauteur / 1.5, 140, 40])



            else:
                pg.draw.rect(screen, couleur_claire, [longueur / 2.2, hauteur / 1.5, 140, 40])

                # superimposing the text onto our button
            screen.blit(quit, (longueur / 2.2 + 14, hauteur / 1.5 + 10))

            # updates the frames of the game
            pg.display.update()

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

        if joueurs[0].vie == 0 or joueurs[1].vie == 0 :
            game.partie = False
            fin.partie = True

        pg.display.update()
        game.time += 1

    while modesolo.partie:

        modesolo.clock.tick(modesolo.frq)
        modesolo.fen.blit(modesolo.fond, (0, 0))

        modesolo.partie = getevents(joueurs2, sys, modesolo.time)

        # Ajout de bonus à intervalle aléatoire

        if modesolo.time - modesolo.tb >= modesolo.cd and len(modesolo.bonus) <= 5:
            modesolo.bonus.append(Bonus(modesolo.fenx))
            cd = uniform(7 * modesolo.frq, 14 * modesolo.frq)
            tb = modesolo.time

        for indice in range(1):
            t = joueurs[indice]
            tir = True

            t.shield = modesolo.time - t.t_shield <= 5 * modesolo.frq

            for b in t.balle:
                if not b.tir:

                    # On dit qu'au moins une balle n'est pas tirée

                    tir = False

                    # On met à jour la position de la balle et son angle de tir si elle n'est pas tirée

                    maj_balle(t, b, modesolo.screen, indice)

                # Dans le cas où la balle est tirée

                else:
                    # On met à jour sa position en fonction de la trajectoire de tir

                    tir_balle(b, modesolo.time, modesolo.fen)

                # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

                touche_ennemi(b, adv)

                # On vérifie si la balle touche un bonus

                touche_bonus(b, t, adv, modesolo)

            if modesolo.time - t.freezeT > 3 * 60 or t.shield:
                t.freeze = False

            if not tir:
                # On affiche la trajectoire de tir

                traj(t, t.balle[-1], modesolo.fen)

            move(t, modesolo.fen, tir)

            t.affiche_vie(modesolo.fen)

        # Affiche les bonus disponibles.
        for bon in modesolo.bonus:
            modesolo.fen.blit(bon.image, [bon.x, bon.y])

        if joueurs[0].vie == 0 or joueurs[1].vie == 0:
            modesolo.partie = False
            fin.partie = True

        pg.display.update()
        modesolo.time += 1

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

        res = (fin.fenx, fin.feny)

        screen = pg.display.set_mode(res)

        couleur = (255, 255, 255)

        couleur_sombre = (36, 63, 93)
        couleur_claire = (61, 72, 77)
        longueur = screen.get_width()
        hauteur = screen.get_height()

        smallfont = pg.font.SysFont('Cooper', 35)
        fond = pg.transform.scale(pg.image.load("fond_menu.png"), (fin.fenx, fin.feny)).convert()
        quit = smallfont.render('QUITTER', True, couleur)
        goMenu = smallfont.render('MENU', True, couleur)
        while fin.partie:
            screen.blit(fond, [0, 0])
            for ev in pg.event.get():

                if ev.type == pg.QUIT:
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:

                    if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (
                            hauteur / 1.5 <= mouse[1] <= hauteur / 1.5 + 40):
                        sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (
                            hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                        menu.partie = True
                        fin.partie = False

            # coordonnes de la souris dans un tuple
            mouse = pg.mouse.get_pos()

            # quand la souris passe sur le bouton la couleur change
            if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (hauteur / 3 <= mouse[1] <= hauteur / 3 + 40):
                pg.draw.rect(screen, couleur_sombre, [longueur / 2.2, hauteur / 3, 140, 40])

            else:
                pg.draw.rect(screen, couleur_claire, [longueur / 2.2, hauteur / 3, 140, 40])
            screen.blit(goMenu, (longueur / 2.2 + 28, hauteur / 3 + 10))

            if (longueur / 2.2 <= mouse[0] <= longueur / 2.2 + 140) and (hauteur / 1.5 <= mouse[1] <= hauteur / 1.5 + 40):
                pg.draw.rect(screen, couleur_sombre, [longueur / 2.2, hauteur / 1.5, 140, 40])



            else:
                pg.draw.rect(screen, couleur_claire, [longueur / 2.2, hauteur / 1.5, 140, 40])

                # superimposing the text onto our button
            screen.blit(quit, (longueur / 2.2 + 14, hauteur / 1.5 + 10))

            # updates the frames of the game
            pg.display.update()