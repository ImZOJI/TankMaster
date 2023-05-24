import tank as char
from bonus import*
import game as multi
import modesolo as solo
import menu as men # obligé de l'importer comme ça il y avait un problème quand je l'importais comme les autres
from fin import*
from cible import*
import sys


def maj_balle(tank, ball, screen, joueur):
    """
    :param tank: Tank
    :param ball: balle
    :param screen: tab
    :param joueur: int
    :return:
    Fonction qui permet de mettre à jour la position et l'angle de tir de la balle lorsqu'elle n'est pas tirée.
    """
    ball.posx = tank.posx + ((60 * screen[0] / 1080) * ((joueur + 1) % 2))
    ball.positionInitiale = ball.posx
    ball.posy = tank.posy + (20 * screen[1] / 675)
    ball.angle = tank.angle


def dessineTrajectoire(tank, ball, fen):
    """
    :param tank: Tank
    :param ball: balle
    :param fen: pg.display
    :return:
    Fonction qui met à jour et affiche la trajectoire de tir.
    """
    if not tank.freeze:
        if tank.plus:
            tank.angle_plus()
        if tank.moins:
            tank.angle_moins()
        ball.affiche(fen)


def tir_balle(ball, time, fen):
    """
    :param ball: Balle
    :param time: int
    :param fen: pg.display
    :return:
    Fonction qui permet de mettre à jour la position de la bale lorsqu'elle est tirée.
    """

    ball.shoot(time)
    ball.hitbox = (ball.posx, ball.posy, ball.size, ball.size)

    # On affiche la balle

    fen.blit(ball.image, (ball.posx, ball.posy))


def touche_ennemi(ball, adversaire):
    """
    :param ball: Balle
    :param adversaire: tank
    :return:
    Fonction quio permet de retirer de la vie si l'adversaire est touché.
    """
    if adversaire.hitbox[0] < ball.posx + ball.size / 2 < adversaire.hitbox[0] + adversaire.hitbox[2] and \
            adversaire.hitbox[1] < ball.posy + ball.size / 2 < adversaire.hitbox[1] + adversaire.hitbox[3]:
        ball.tir = False
        pg.mixer.Sound("exploion.mp3").play()
        if not adversaire.shield:
            adversaire.vie -= 1

def touche_cible(ball, modesolo) :
    if modesolo.cble.hitbox[0] < ball.posx + ball.size / 2 < modesolo.cble.hitbox[2] and modesolo.cble.hitbox[1] <\
            ball.posy + ball.size / 2 < modesolo.cble.hitbox[3]:
        ball.tir = False
        modesolo.score += 1
        modesolo.cble = cible(modesolo.fenx)


def touche_bonus(ball, tank, adversaire, partie):
    i = 0
    while i < len(partie.bonus):
        bon = partie.bonus[i]
        if bon.hitbox[0] < ball.posx + ball.size / 2 < bon.hitbox[2] and bon.hitbox[1] < ball.posy + ball.size / 2 < \
                bon.hitbox[3]:

            # On applique le bonus en fonction de son type

            match bon.type:
                case 0:
                    adversaire.freeze = True
                    adversaire.freezeT = partie.time
                case 1:
                    tank.balle.append(char.balle(tank.propx, tank.propy))
                case 2:
                    tank.vit += 3
                case 3:
                    for bll in tank.balle:
                        bll.multiplicateur += 0.25
                case 4:
                    tank.t_shield = partie.time

            # On supprime le bonus touché

            partie.bonus = partie.bonus[:i] + partie.bonus[i + 1:]
        i += 1


def deplace(tank, tir):
    if not tank.freeze:
        if not tir:
            if tank.g:
                tank.gauche()
            if tank.d:
                tank.droite()
            tank.hitbox = (tank.posx, tank.posy, tank.size, tank.size)

def affiche_tank(tank,fen):
    if not tank.freeze:
        if not tank.shield:
            fen.blit(tank.image, [tank.posx, tank.posy])
        else :
            fen.blit(tank.shield_img, [tank.posx, tank.posy])
    else :
        fen.blit(tank.freeze_img, [tank.posx, tank.posy])


def keydown(event, joueurs, sys, time,):
    partie = True
    if event.type == pg.QUIT:
        partie = False
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
                for ball in joueurs[0].balle:
                    if not ball.tir:
                        ball.tempsInitial = time
                        shotSound = pg.mixer.Sound("shot.mp3")
                        shotSound.set_volume(0.3)
                        shotSound.play()
                        ball.tir = True
                        break
        if event.key == pg.K_RETURN:
            if not joueurs[1].freeze:
                for ball in joueurs[1].balle:
                    if not ball.tir:
                        ball.tempsInitial = time
                        shotSound = pg.mixer.Sound("shot.mp3")
                        shotSound.set_volume(0.3)
                        shotSound.play()
                        ball.tir = True
                        break
    return partie


def keyup(event, joueurs):
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


def getevents(joueurs, sys, time):
    partie = True
    for event in pg.event.get():
        partie = keydown(event, joueurs, sys, time)
        keyup(event, joueurs)
    return partie


def explosion(fen):
    spritesheet = pg.image.load("explosion.png").convert_alpha()
    img = spritesheet.subsurface((0, 0, 384, 384))


def mainMenu(fen):
    screen = [fenx, feny] = fen.get_size()
    menu = men.menu(screen)
    fond = pg.transform.scale(pg.image.load("fond_menu.png"), (menu.fenx, menu.feny)).convert()

    while menu.partie:

        fen.blit(fond, [0, 0])

        # coordonnes de la souris dans un tuple
        mouse = pg.mouse.get_pos()
        eventMenu(menu, mouse, fen)

        font = pg.font.Font('INVASION2000.TTF', 150)
        tankmaster = font.render('TANKMASTER', True, (255,255,255))
        fen.blit(tankmaster, (menu.fenx / 2 - 510 , 100))

        dessineBoutons(menu, fen, mouse)

        # updates the frames of the game
        pg.display.update()


def eventMenu(menu, mouse, fen):
    for ev in pg.event.get():

        if ev.type == pg.QUIT:
            sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:

            if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                    menu.feny / 1.5 <= mouse[1] <= menu.feny / 1.5 + 40):
                sys.exit()
            if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                    menu.feny / 3 <= mouse[1] <= menu.feny / 3 + 40):
                partieMulti(fen)
            if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                    menu.feny / 3 + 50<= mouse[1] <= menu.feny / 3 + 90):
                partieSolo(fen)


def dessineBoutons(menu, fen, mouse):
        couleur = (255, 255, 255)

        couleur_sombre = (36, 63, 93)
        couleur_claire = (61, 72, 77)
        smallfont = pg.font.SysFont('Cooper', 35)
        fond = pg.transform.scale(pg.image.load("fond_menu.png"), (menu.fenx, menu.feny)).convert()
        quit = smallfont.render('QUITTER', True, couleur)
        jouer = smallfont.render('MULTI 2J', True, couleur)
        solo = smallfont.render('SOLO', True, couleur)

        if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (menu.feny / 3 <= mouse[1] <= menu.feny / 3 + 40):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2, menu.feny / 3, 140, 40])
        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2, menu.feny / 3, 140, 40])
        fen.blit(jouer, (menu.fenx / 2.2 + 18, menu.feny / 3 + 10))

        if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                    menu.feny / 3 + 50<= mouse[1] <= menu.feny / 3 + 90):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2, menu.feny / 3 + 50, 140, 40])
        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2 , menu.feny / 3 + 50, 140, 40])
        fen.blit(solo, (menu.fenx / 2.2 + 34, menu.feny / 3 + 60))

        if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (menu.feny / 1.5 <= mouse[1] <= menu.feny /
                                                                       1.5 + 40):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2, menu.feny / 1.5, 140, 40])
        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2, menu.feny / 1.5, 140, 40])
        fen.blit(quit, (menu.fenx / 2.2 + 14, menu.feny / 1.5 + 10))


def partieSolo(fen):
    screen = [fenx, feny] = fen.get_size()
    modesolo = solo.modesolo(screen)
    tankSolo = char.tank("tank1.png", 1, modesolo.fenx, modesolo.feny)
    joueurSolo = [tankSolo, tankSolo]

    while modesolo.time < 0 * modesolo.frq:
        modesolo.clock.tick(modesolo.frq)
        fen.blit(modesolo.fond, (0, 0))

        modesolo.partie = getevents(joueurSolo, sys, modesolo.time)

        t = joueurSolo[0]
        tir = True


        for b in t.balle:
            if not b.tir:

                # On dit qu'au moins une balle n'est pas tirée

                tir = False

                # On met à jour la position de la balle et son angle de tir si elle n'est pas tirée

                maj_balle(t, b, modesolo.screen, 0)

            # Dans le cas où la balle est tirée

            else :
                # On met à jour sa position en fonction de la trajectoire de tir

                tir_balle(b, modesolo.time, fen)

                touche_cible(b, modesolo)

        if not tir:
            # On affiche la trajectoire de tir

            dessineTrajectoire(t, t.balle[-1], fen)

        deplace(t, tir)

        affiche_tank(t, fen)

        fen.blit(modesolo.cble.image, (modesolo.cble.x, modesolo.cble.y))

        font = pg.font.SysFont("arial", 48)
        minutes = modesolo.time // 3600
        secondes = modesolo.time // 60
        temps = font.render(str(minutes // 10)+str(minutes % 10)+" : "+str(secondes // 10)+str(secondes % 10),
                            True, "white", )
        fen.blit(temps, (fenx - 300, 50))
        score = font.render(str(modesolo.score // 10)+str(modesolo.score % 10), True, "white")
        fen.blit(score, (10, 50))


        pg.display.update()
        modesolo.time += 1

    finSolo(fen, modesolo.score)

def menuFin(fen):
    screen = [fenx, feny] = fen.get_size()
    fini = True
    couleur = (255, 255, 255)
    fond = pg.transform.scale(pg.image.load("gameover.jpg"), (fenx, feny)).convert()
    couleur_sombre = (36, 63, 93)
    couleur_claire = (61, 72, 77)
    smallfont = pg.font.SysFont('Cooper', 35)
    jouer = smallfont.render('CONTINUE', True, couleur)

    while fini:
        fen.blit(fond, (0,0))
        mouse = pg.mouse.get_pos()
        if (fenx / 2.2 <= mouse[0] <= fenx / 2.2 + 140) and (feny / 1.2 <= mouse[1] <= feny / 1.2 + 40):
            pg.draw.rect(fen, couleur_sombre, [fenx / 2.2, feny / 1.2, 140, 40])
        else:
            pg.draw.rect(fen, couleur_claire, [fenx / 2.2, feny / 1.2, 140, 40])
        fen.blit(jouer, (fenx / 2.2 + 5, feny / 1.2 + 10))
        pg.display.update()
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if (fenx / 2.2 <= mouse[0] <= fenx / 2.2 + 140) and (feny / 1.2 <= mouse[1] <= feny / 1.2 + 40):
                    mainMenu(fen)


def finSolo(fen, score):
    screen = [fenx, feny] = fen.get_size()
    fini = True
    couleur = (255, 255, 255)
    fond = pg.transform.scale(pg.image.load("gameover.jpg"), (fenx, feny)).convert()
    couleur_sombre = (36, 63, 93)
    couleur_claire = (61, 72, 77)
    smallfont = pg.font.SysFont('Cooper', 35)
    jouer = smallfont.render('CONTINUE', True, couleur)

    while fini:
        fen.blit(fond, (0,0))
        mouse = pg.mouse.get_pos()
        if (fenx / 2.2 <= mouse[0] <= fenx / 2.2 + 140) and (feny / 1.2 <= mouse[1] <= feny / 1.2 + 40):
            pg.draw.rect(fen, couleur_sombre, [fenx / 2.2, feny / 1.2, 140, 40])
        else:
            pg.draw.rect(fen, couleur_claire, [fenx / 2.2, feny / 1.2, 140, 40])
        fen.blit(jouer, (fenx / 2.2 + 5, feny / 1.2 + 10))

        font = pg.font.Font("INVASION2000.TTF", 128)
        scoreTxt = font.render("SCORE : " + str(score // 10) + str(score % 10), True, "white")
        fen.blit(scoreTxt, (250 * (fenx / 1080), 100 * (feny / 675)))

        pg.display.update()
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if (fenx / 2.2 <= mouse[0] <= fenx / 2.2 + 140) and (feny / 1.2 <= mouse[1] <= feny / 1.2 + 40):
                    mainMenu(fen)


def partieMulti(fen):
    screen = [fenx, feny] = fen.get_size()
    game = multi.game(screen)
    game.partie = True
    tank1 = char.tank("tank1.png", 1, game.fenx, game.feny)
    tank2 = char.tank("tank2.png", 2, game.fenx, game.feny)
    joueurs = [tank1, tank2]
    joueurs[1].angle = 136

    while game.partie :
        game.clock.tick(game.frq)
        fen.blit(game.fond, (0, 0))

        game.partie = getevents(joueurs, sys, game.time)

        # Ajout de bonus à intervalle aléatoire

        if game.time - game.lastBonusTime >= game.couldown and len(game.bonus) <= 5:
            game.bonus.append(Bonus(game.fenx))
            game.cooldown = uniform(7 * game.frq, 14 * game.frq)
            game.lastBonusTime = game.time

        for indice in range(2) :
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

                else :
                    # On met à jour sa position en fonction de la trajectoire de tir

                    tir_balle(ball, game.time, fen)

                # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

                touche_ennemi(ball, adv)

                # On vérifie si la balle touche un bonus

                touche_bonus(ball, tank, adv, game)

            if game.time - tank.freezeT > 3 * 60 or tank.shield:
                tank.freeze = False

            if not tir :
                # On affiche la trajectoire de tir

                dessineTrajectoire(tank, tank.balle[-1], fen)

            deplace(tank, tir)

            affiche_tank(tank, fen)

            tank.affiche_vie(fen)

            if joueurs[0].vie == 0 or joueurs[1].vie == 0:
                game.partie = False

        # Affiche les bonus disponibles.
        for bon in game.bonus :
            fen.blit(bon.image, [bon.x, bon.y])

        pg.display.update()
        game.time += 1
    menuFin(fen)

