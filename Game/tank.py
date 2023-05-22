from balle import*

class tank:
    def __init__(self, img: str, j: int, fenx, feny):
        self.propx = fenx / 1080
        self.propy = feny / 675
        self.numeroJoueur = j
        self.posx = (10+996*(j-1)) * self.propx
        self.posy = 500 * self.propy
        self.size = 64 * self.propx
        self.image = pg.transform.scale(pg.image.load(img), (self.size, self.size))
        self.balle = [balle(self.propx, self.propy)]
        self.g = False
        self.d = False
        self.plus = False
        self.moins = False
        self.vie = 5
        self.hitbox = (self.posx, self.posy, self.size, self.size)
        self.angle = self.balle[0].angle

        # Attributs pour application de bonus


        self.freeze_img = pg.transform.scale(pg.image.load(img[:5] + "_gel.png"), (self.size, self.size))
        self.freeze = False
        self.freezeT = 0
        self.vit = 3
        self.t_shield = 0
        self.shield = False
        self.shield_img = pg.transform.scale(pg.image.load(img[:5] + "_shield.png"), (self.size, self.size))

    def gauche(self):
        if self.numeroJoueur == 1 and self.posx > 10 * self.propx:
            self.posx -= self.vit * self.propx
        elif self.numeroJoueur == 2 and self.posx > 550 * self.propx:
            self.posx -= self.vit * self.propx

    def droite(self):
        if self.numeroJoueur == 1 and self.posx < 467 * self.propx:
            self.posx += self.vit * self.propx
        if self.numeroJoueur == 2 and self.posx < 1006 * self.propx:
            self.posx += self.vit * self.propx

    def affiche_vie(self,fen):
        coeur = pg.transform.scale(pg.image.load("coeur.png"), (self.size, self.size)).convert_alpha()
        for i in range(self.vie):
            if self.numeroJoueur == 1:
                fen.blit(coeur.convert_alpha(), ((10 + i* 74) * self.propx, 10 * self.propy))
            else:
                fen.blit(coeur.convert_alpha(), (((1080-10-64) - i* 74) * self.propx, 10 * self.propy))

    def angle_plus(self):
        if self.angle < 89:
            self.angle += 1
        elif self.angle > 91:
            self.angle -= 1

    def angle_moins(self):
        if 90 > self.angle > 1:
            self.angle -= 1
        elif 179 > self.angle > 90:
            self.angle += 1
