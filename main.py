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

#Definition de la p
police_c_a_r = pg.font.Font("effets/polices/turok.ttf", 200)
police_score = pg.font.Font("effets/polices/turok.ttf", 30)

#Fonction pour dessiner du texte
def dessiner_texte(texte, police, couleur, x, y):
    image = police.render(texte, True, couleur)
    ecran.blit(image, (x, y))

#Definition variables de jeu
compte_rebours_intro = 3
derniere_maj_compte_rebours = pg.time.get_ticks()
score = [0, 0] #[j1, j2]
combat_termine = False
COOLDOWN_COMBAT_TERMINE = 3000

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

#Charger le texte de victoire
im_vict = pg.image.load("effets/images/icones/victory.png").convert_alpha()

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
combattant_1 = Combattant(1, 200, 310, False, GUERRIER_DONNEES, spritesheet_guerrier, GUERRIER_NBRE_FRAMES)
combattant_2 = Combattant(2, 700, 310, True, MAGICIEN_DONNEES, spritesheet_magicien, MAGICIEN_NBRE_FRAMES)

#Boucle de jeu
lance = True
while lance:
    horloge.tick(fps)

    #Dessiner le fond
    dessiner_fond()

    #Dessiner les barres de vie
    dessiner_barres(combattant_1.sante, 20, 20)
    dessiner_barres(combattant_2.sante, 580, 20)
    dessiner_texte("J1 : " + str(score[0]), police_score, ROUGE, 20, 60)
    dessiner_texte("J2 : " + str(score[1]), police_score, ROUGE, 580, 60)


    #Maj compte a rebours
    if compte_rebours_intro <= 0:
        #Bouger les combattants
        combattant_1.bouger(LARG_ECRAN, HAUT_ECRAN, ecran, combattant_2, combat_termine)
        combattant_2.bouger(LARG_ECRAN, HAUT_ECRAN, ecran, combattant_1, combat_termine)
    else:
        dessiner_texte(str(compte_rebours_intro), police_c_a_r, ROUGE, LARG_ECRAN / 2 - 40, HAUT_ECRAN / 3.5)
        if (pg.time.get_ticks() - derniere_maj_compte_rebours) >= 700:
            compte_rebours_intro -= 1
            derniere_maj_compte_rebours = pg.time.get_ticks()

    #Maj des combattants
    combattant_1.maj()
    combattant_2.maj()

    #Dessiner les combattants
    combattant_1.dessiner(ecran)
    combattant_2.dessiner(ecran)

    #Cheque si un joueur est mort
    if combat_termine == False:
        if combattant_1.vivant == False:
            score[1] += 1
            combat_termine = True
            fin_de_combat = pg.time.get_ticks()
        elif combattant_2.vivant == False:
            score[0] += 1
            combat_termine = True
            fin_de_combat = pg.time.get_ticks()
    else:
        ecran.blit(im_vict, (360, 150))
        if pg.time.get_ticks() - fin_de_combat > COOLDOWN_COMBAT_TERMINE:
            combat_termine = False
            compte_rebours_intro = 3
            combattant_1 = Combattant(1, 200, 310, False, GUERRIER_DONNEES, spritesheet_guerrier, GUERRIER_NBRE_FRAMES)
            combattant_2 = Combattant(2, 700, 310, True, MAGICIEN_DONNEES, spritesheet_magicien, MAGICIEN_NBRE_FRAMES)

    #Gestion des evenements
    for evenement in pg.event.get():
        if evenement.type == pg.QUIT:
            lance = False

    #Maj de l'ecran
    pg.display.update()

#Fermer pygame
pg.quit()