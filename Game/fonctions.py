from tank import *


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
    ball.pos0 = ball.posx
    ball.posy = tank.posy + (20 * screen[1] / 675)
    ball.angle = tank.angle


def traj(tank, ball, fen):
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
        if not adversaire.shield:
            adversaire.vie -= 1


def touche_bonus(ball, tank, adversaire, bonus, time):
    i = 0
    while i < len(bonus):
        bon = bonus[i]
        if bon.hitbox[0] < ball.posx < bon.hitbox[2] and bon.hitbox[1] < ball.posy < \
                bon.hitbox[3]:

            # On applique le bonus en fonction de son type

            match bon.type:
                case 0:
                    adversaire.freeze = True
                    adversaire.freezeT = time
                case 1:
                    tank.balle.append(balle(tank.propx, tank.propy))
                case 2:
                    tank.vit += 3
                case 3:
                    for bll in tank.balle:
                        bll.mult += 0.25
                case 4:
                    tank.t_shield = time

            # On supprime le bonus touché

            bonus = bonus[:i] + bonus[i + 1:]
        i += 1


def move(tank, fen, tir):
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
