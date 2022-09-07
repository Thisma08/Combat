import pygame as pg

class Combattant():
    def __init__(self, x, y, flip, donnees, spritesheet, frames_animation):
        self.rect = pg.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.saut = False
        self.attaque = False
        self.type_attaque = 0
        self.sante = 100
        self.flip = flip
        self.taille = donnees[0]
        self.echelle_image = donnees[1]
        self.decalage = donnees[2]
        self.liste_animation = self.charger_images(spritesheet, frames_animation)
        #0: debout / 1: course / 2: saut / 3: attaque1 / 4: attaque 2 / 5: coup pris / 6: ko
        self.action = 0
        self.indice_frame = 0
        self.image = self.liste_animation[self.action][self.indice_frame]

    def charger_images(self, spritesheet, frames_animation):
        #Extraction d'images de la spritesheet
        liste_animation = []
        for y, animation in enumerate(frames_animation):
            liste_im_temp = []
            for x in range(animation):
                im_temp = spritesheet.subsurface(x * self.taille, y * self.taille, self.taille, self.taille)
                liste_im_temp.append(pg.transform.scale(im_temp, (self.taille * self.echelle_image, self.taille * self.echelle_image)))
            liste_animation.append(liste_im_temp)
        return liste_animation

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

        #S'assurer que les 2 joueurs se font face
        if cible.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Maj de la position du joueur
        self.rect.x += dx
        self.rect.y += dy

    def dessiner(self, surface):
        image = pg.transform.flip(self.image, self.flip, False)
        pg.draw.rect(surface, (0, 255, 0), self.rect)
        surface.blit(image, (self.rect.x - (self.decalage[0] * self.echelle_image), self.rect.y - (self.decalage[1] * self.echelle_image)))

    def attaquer(self, surface, cible):
        self.attaque = True
        rect_attaque = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if rect_attaque.colliderect(cible.rect):
            cible.sante -= 10
        pg.draw.rect(surface, (255, 0, 0), rect_attaque)
