import pygame as pg

class Combattant():
    def __init__(self, x, y):
        self.rect = pg.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.saut = False
        self.attaque = False
        self.type_attaque = 0

    def bouger(self, larg_ecran, haut_ecran, surface, cible):
        VITESSE = 5
        GRAVITE = 2
        dx = 0
        dy = 0

        #Touches
        touche = pg.key.get_pressed()

        #Ne pas bouger quand attaque
        if self.attaque == False:
            #Mouvement
            if touche[pg.K_q]:
                dx = -VITESSE
            if touche[pg.K_d]:
                dx = VITESSE

            #Saut
            if touche[pg.K_z] and self.saut == False:
                self.vel_y = -30
                self.saut = True

            #Attaque
            if touche[pg.K_r] or touche[pg.K_t]:
                self.attaquer(surface, cible)
                #Type d'attaque
                if touche[pg.K_r]:
                    self.type_attaque = 1
                if touche[pg.K_t]:
                    self.type_attaque = 2

        #Appliquer gravité
        self.vel_y += GRAVITE
        dy += self.vel_y

        #Garder le combattant sur l'ecran
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > larg_ecran:
            dx = larg_ecran - self.rect.right
        if self.rect.bottom + dy > haut_ecran - 110:
            self.vel_y = 0
            dy = haut_ecran - 110 - self.rect.bottom
            self.saut = False

        #Maj de la position du joueur
        self.rect.x += dx
        self.rect.y += dy

    def dessiner(self, surface):
        pg.draw.rect(surface, (0, 255, 0), self.rect)

    def attaquer(self, surface, cible):
        self.attaque = True
        rect_attaque = pg.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if rect_attaque.colliderect(cible.rect):
            print("Coup infligé")
        pg.draw.rect(surface, (255, 0, 0), rect_attaque)
