import pygame as pg

class Combattant():
    def __init__(self, joueur, x, y, flip, donnees, spritesheet, frames_animation):
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
        self.temps_de_maj = pg.time.get_ticks()
        self.court = False
        self.cooldown_attaque = 0
        self.coup = False
        self.vivant = True
        self.joueur = joueur

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

    def bouger(self, larg_ecran, haut_ecran, surface, cible, combat_termine):
        VITESSE = 5
        GRAVITE = 2
        dx = 0
        dy = 0
        self.court = False
        self.type_attaque = 0

        #Touches
        touche = pg.key.get_pressed()

        #Ne pas bouger quand attaque
        #joueur 1
        if self.joueur == 1:
            if self.attaque == False and self.vivant == True and combat_termine == False:
                #Mouvement
                if touche[pg.K_q]:
                    dx = -VITESSE
                    self.court = True
                if touche[pg.K_d]:
                    dx = VITESSE
                    self.court = True

                #Saut
                if touche[pg.K_z] and self.saut == False:
                    self.vel_y = -30
                    self.saut = True

                #Attaque
                if touche[pg.K_r] or touche[pg.K_t]:
                    self.attaquer(cible)
                    #Type d'attaque
                    if touche[pg.K_r]:
                        self.type_attaque = 1
                    if touche[pg.K_t]:
                        self.type_attaque = 2

        if self.joueur == 2:
            if self.attaque == False and self.vivant == True and combat_termine == False:
                #Mouvement
                if touche[pg.K_LEFT]:
                    dx = -VITESSE
                    self.court = True
                if touche[pg.K_RIGHT]:
                    dx = VITESSE
                    self.court = True

                #Saut
                if touche[pg.K_UP] and self.saut == False:
                    self.vel_y = -30
                    self.saut = True

                #Attaque
                if touche[pg.K_KP1] or touche[pg.K_KP2]:
                    self.attaquer(cible)
                    #Type d'attaque
                    if touche[pg.K_KP1]:
                        self.type_attaque = 1
                    if touche[pg.K_KP2]:
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

        #Appliquer le cooldown d'attaque
        if self.cooldown_attaque > 0:
            self.cooldown_attaque -= 1

        #Maj de la position du joueur
        self.rect.x += dx
        self.rect.y += dy

    def dessiner(self, surface):
        image = pg.transform.flip(self.image, self.flip, False)
        surface.blit(image, (self.rect.x - (self.decalage[0] * self.echelle_image), self.rect.y - (self.decalage[1] * self.echelle_image)))

    def attaquer(self, cible):
        if self.cooldown_attaque == 0:
            self.attaque = True
            rect_attaque = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if rect_attaque.colliderect(cible.rect):
                cible.sante -= 10
                cible.coup = True

    #Maj_animations
    def maj(self):
        #Quelle action le joueur fait-il ?
        if self.sante <= 0:
            self.sante = 0
            self.vivant = False
            self.maj_action(6)
        elif self.coup == True:
            self.maj_action(5)
        elif self.attaque == True:
            if self.type_attaque == 1:
                self.maj_action(3)
            elif self.type_attaque == 2:
                self.maj_action(4)
        elif self.saut == True:
            self.maj_action(2)
        elif self.court == True :
            self.maj_action(1)
        else:
            self.maj_action(0)
        #0: debout / 1: course / 2: saut / 3: attaque 1 / 4: attaque 2 / 5: coup pris / 6: ko

        cooldown_anim = 50
        self.image = self.liste_animation[self.action][self.indice_frame]

        #Cheque si assez de temps est passé depuis la derniere maj
        if pg.time.get_ticks() - self.temps_de_maj > cooldown_anim:
            self.indice_frame += 1
            self.temps_de_maj = pg.time.get_ticks()

        #Cheque si l'animation est finie
        if self.indice_frame >= len(self.liste_animation[self.action]):
            #Si le joueur est mort alors ne plus l'animer
            if self.vivant == False:
                self.indice_frame = len(self.liste_animation[self.action]) - 1
            else:
                self.indice_frame = 0
                #Cheque si une attaque est finie
                if self.action == 3 or self.action == 4:
                    self.attaque = False
                    self.cooldown_attaque = 50
                # Cheque si un coup a ete pris
                if self.action == 5:
                    self.coup = False
                    #Si le joueur etait au milieu d'une attaque, celle ci est stoppée
                    self.attaque = False
                    self.cooldown_attaque = 20

    def maj_action(self, nouv_action):
        #La nouvelle action est elle differente de la precedente ?
        if nouv_action != self.action:
            self.action = nouv_action
            #maj parametres d'animation
            self.indice_frame = 0
            self.temps_de_maj = pg.time.get_ticks()