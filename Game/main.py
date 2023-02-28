from tank import *
from bonus import *
from fonctions import *


pg.init()

frq = 60
clock = pg.time.Clock()
time = 0

partie = True
fen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
'''fen = pg.display.set_mode((1080, 675))'''
fenx, feny = fen.get_size()

fond = pg.transform.scale(pg.image.load("background.jpeg"), (fenx, feny)).convert()

tank1 = tank("tank1.png", 1, fenx, feny)
tank2 = tank("tank2.png", 2, fenx, feny)
joueurs = [tank1, tank2]
joueurs[1].angle = 136

bonus = []
cd = 0 # temps avant l'apparition du prochain
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

                b.posx = t.posx + ((60 * fenx / 1080) * ((indice + 1) % 2))
                b.pos0 = b.posx
                b.posy = t.posy + (20 * feny / 675)
                b.angle = t.angle

                # On affiche la balle

                if not t.freeze:
                    if t.plus:
                        t.angle_plus()
                    if t.moins:
                        t.angle_moins()
                    b.affiche(fen)

            # Dans le cas où la balle est tirée

            else:

                # On met à jour sa position en fonction de la trajectoire de tir

                b.shoot(time)
                b.hitbox = (b.posx, b.posy, b.size, b.size)

                # On affiche la balle

                fen.blit(b.image, (b.posx, b.posy))

            # On vérifie si la balle touche l'adversaire s'il n'est pas invincible

            if adv.hitbox[0] < b.posx < adv.hitbox[0] + adv.hitbox[2] and adv.hitbox[1] < b.posy < \
                    adv.hitbox[1] + adv.hitbox[3]:
                b.tir = False
                if  not adv.shield:
                    adv.vie -= 1

            # On vérifie si la balle touche un bonus

            i = 0
            while i < len(bonus):
                bon = bonus[i]
                if bon.hitbox[0] < b.posx < bon.hitbox[2] and bon.hitbox[1] < b.posy < \
                        bon.hitbox[3]:

                    # On applique le bonus en fonction de son type

                    match bon.type:
                        case 0:
                            adv.freeze = True
                            adv.freezeT = time
                        case 1:
                            t.balle.append(balle(t.propx, t.propy))
                        case 2:
                            t.vit += 3
                        case 3:
                            for bll in t.balle:
                                bll.mult += 0.25
                        case 4:
                            t.t_shield = time

                    # On supprime le bonus touché

                    bonus = bonus[:i] + bonus[i + 1:]
                i += 1

        if time - t.freezeT > 3 * 60 or t.shield:
            t.freeze = False

        if not t.freeze:
            if not tir:
                if t.g :
                    t.gauche()
                if t.d :
                    t.droite()
                t.hitbox = (t.posx, t.posy, t.size, t.size)
            if not t.shield:
                fen.blit(t.image, [t.posx, t.posy])
            else:
                fen.blit(t.shield_img, [t.posx, t.posy])
        else:
            fen.blit(t.freeze_img, [t.posx, t.posy])

        t.affiche_vie(fen)

    for bon in bonus:
        fen.blit(bon.image, [bon.x, bon.y])
    pg.display.update()
    time += 1
