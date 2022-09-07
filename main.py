import pygame as pg

pg.init()
from combattant import Combattant

#Creation fenetre
LARG_ECRAN = 1000
HAUT_ECRAN = 600

ecran = pg.display.set_mode((LARG_ECRAN, HAUT_ECRAN))
pg.display.set_caption("Combat")

#Definir la framerate
horloge = pg.time.Clock()
fps = 60

#Definir couleurs
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
BLANC = (255, 255, 255)

#Definir les variables de combattant
GUERRIER_TAILLE = 162
GUERRIER_ECHELLE = 4
GUERRIER_DECALAGE = [72, 56]
GUERRIER_DONNEES = [GUERRIER_TAILLE, GUERRIER_ECHELLE, GUERRIER_DECALAGE]
MAGICIEN_TAILLE = 250
MAGICIEN_ECHELLE = 3
MAGICIEN_DECALAGE = [112, 107]
MAGICIEN_DONNEES = [MAGICIEN_TAILLE, MAGICIEN_ECHELLE, MAGICIEN_DECALAGE]



#Charger l'image de fond
im_fond = pg.image.load("effets/images/fond/fond.jpg").convert_alpha()

#Charger la spritesheet
spritesheet_guerrier = pg.image.load("effets/images/guerrier/sprites/guerrier.png").convert_alpha()
spritesheet_magicien = pg.image.load("effets/images/magicien/sprites/magicien.png").convert_alpha()

#Definir le nombre d'images dans chaque animation
GUERRIER_NBRE_FRAMES = [10, 8, 1, 7, 7, 3, 7]
MAGICIEN_NBRE_FRAMES = [8, 8, 1, 8, 8, 3, 7]

#Fonction dessinant le fond
def dessiner_fond():
    im_fond_echelle = pg.transform.scale(im_fond, (LARG_ECRAN, HAUT_ECRAN))
    ecran.blit(im_fond_echelle, (0, 0))

#Fonction dessinant les barres de vie
def dessiner_barres(sante, x, y):
    ratio = sante / 100
    pg.draw.rect(ecran, BLANC, (x - 3, y - 3, 406, 36))
    pg.draw.rect(ecran, ROUGE, (x, y, 400, 30))
    pg.draw.rect(ecran, JAUNE, (x, y, 400 * ratio, 30))

#Creer 2 instances de combattants
combattant_1 = Combattant(200, 310, False, GUERRIER_DONNEES, spritesheet_guerrier, GUERRIER_NBRE_FRAMES)
combattant_2 = Combattant(700, 310, True, MAGICIEN_DONNEES, spritesheet_magicien, MAGICIEN_NBRE_FRAMES)

#Boucle de jeu
lance = True
while lance:
    horloge.tick(fps)

    #Dessiner le fond
    dessiner_fond()

    #Dessiner les barres de vie
    dessiner_barres(combattant_1.sante, 20, 20)
    dessiner_barres(combattant_2.sante, 580, 20)

    #Bouger les combattants
    combattant_1.bouger(LARG_ECRAN, HAUT_ECRAN, ecran, combattant_2)

    #Dessiner les combattants
    combattant_1.dessiner(ecran)
    combattant_2.dessiner(ecran)

    #Gestion des evenements
    for evenement in pg.event.get():
        if evenement.type == pg.QUIT:
            lance = False

    #Maj de l'ecran
    pg.display.update()

#Fermer pygame
pg.quit()