from tank import *
from bonus import*
from game import*
from modesolo import*
from menu import*
from fin import*
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
    if adversaire.hitbox[0] < ball.posx < adversaire.hitbox[0] + adversaire.hitbox[2] and adversaire.hitbox[1] <\
            ball.posy < adversaire.hitbox[1] + adversaire.hitbox[3]:
        ball.tir = False
        pg.mixer.Sound("exploion.mp3").play()
        if not adversaire.shield:
            adversaire.vie -= 1


def touche_bonus(ball, tank, adversaire, partie):
    i = 0
    while i < len(partie.bonus):
        bon = partie.bonus[i]
        if bon.hitbox[0] < ball.posx < bon.hitbox[2] and bon.hitbox[1] < ball.posy < \
                bon.hitbox[3]:

            # On applique le bonus en fonction de son type

            match bon.type:
                case 0:
                    adversaire.freeze = True
                    adversaire.freezeT = partie.time
                case 1:
                    tank.balle.append(balle(tank.propx, tank.propy))
                case 2:
                    tank.vit += 3
                case 3:
                    for bll in tank.balle:
                        bll.multiplicateur += 0.25
                case 4:
                    tank.t_shield = partie.time

            # On supprime le bonus touché

            partie.bonus = partie.bonus[:i] + partie.bonus[i + 1 :]
        i += 1


def deplace(tank, fen, tir):
    if not tank.freeze:
        if not tir:
            if tank.g:
                tank.gauche()
            if tank.d:
                tank.droite()
            tank.hitbox = (tank.posx, tank.posy, tank.size, tank.size)
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


def menu(fen):
    menu = menu(screen)

    while menu.partie:

        couleur = (255, 255, 255)

        couleur_sombre = (36, 63, 93)
        couleur_claire = (61, 72, 77)

        smallfont = pg.font.SysFont('Cooper', 35)
        fond = pg.transform.scale(pg.image.load("fond_menu.png"), (menu.fenx, menu.feny)).convert()
        quit = smallfont.render('QUITTER', True, couleur)
        jouer = smallfont.render('MULTI 2J', True, couleur)
        solo = smallfont.render('SOLO', True, couleur)

        fen.blit(fond, [0, 0])
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:

                if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                        menu.feny / 1.5 <= mouse[1] <= menu.feny / 1.5 + 40):
                    sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (
                        menu.feny / 3 <= mouse[1] <= menu.feny / 3 + 40):
                    game.partie = True
                    menu.partie = False

            if ev.type == pg.MOUSEBUTTONDOWN:
                if (menu.fenx / 2.2 + 150 <= mouse[0] <= menu.fenx / 2.2 + 290) and (
                        menu.feny / 3 <= mouse[1] <= menu.feny / 3 + 40):
                    modesolo.partie = True
                    menu.partie = False

        # coordonnes de la souris dans un tuple
        mouse = pg.mouse.get_pos()

        # quand la souris passe sur le bouton la couleur change
        if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (menu.feny / 3 <= mouse[1] <= menu.feny / 3 + 40):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2, menu.feny / 3, 140, 40])

        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2, menu.feny / 3, 140, 40])
        fen.blit(jouer, (menu.fenx / 2.2 + 18, menu.feny / 3 + 10))

        if (menu.fenx / 2.2 + 150 <= mouse[0] <= menu.fenx / 2.2 + 290) and (menu.feny / 3 <= mouse[1] <= menu.feny /
                                                                             3 + 40):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2 + 150, menu.feny / 3, 140, 40])

        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2 + 150, menu.feny / 3, 140, 40])
        fen.blit(solo, (menu.fenx / 2.2 + 178, menu.feny / 3 + 10))

        if (menu.fenx / 2.2 <= mouse[0] <= menu.fenx / 2.2 + 140) and (menu.feny / 1.5 <= mouse[1] <= menu.feny /
                                                                       1.5 + 40):
            pg.draw.rect(fen, couleur_sombre, [menu.fenx / 2.2, menu.feny / 1.5, 140, 40])



        else:
            pg.draw.rect(fen, couleur_claire, [menu.fenx / 2.2, menu.feny / 1.5, 140, 40])

            # superimposing the text onto our button
        fen.blit(quit, (menu.fenx / 2.2 + 14, menu.feny / 1.5 + 10))

        # updates the frames of the game
        pg.display.update()