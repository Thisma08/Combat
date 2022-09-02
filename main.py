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

#Charger l'image de fond
im_fond = pg.image.load("effets/images/fond/fond.jpg").convert_alpha()

#Fonction dessinant le fond
def dessiner_fond():
    im_fond_echelle = pg.transform.scale(im_fond, (LARG_ECRAN, HAUT_ECRAN))
    ecran.blit(im_fond_echelle, (0, 0))


#Creer 2 instances de combattants
combattant_1 = Combattant(200, 310)
combattant_2 = Combattant(700, 310)

#Boucle de jeu
lance = True
while lance:
    horloge.tick(fps)

    #Dessiner le fond
    dessiner_fond()

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