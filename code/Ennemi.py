import pygame
from code.Config import *
from code.Map import *
import math



class Ennemi:
    def __init__(self, x, y, joueur, carte):
        """
        pre :
            x = position de l'enemi sur l'axe des abscisse (int)
            y = position de l'enemi sur l'axe des ordonné (int)
            joueur = le joueur que l'ennemi devra suivre dans suivre_joueur (objet)
            carte = la carte sur laquelle on joue actuellement
        post :
            /
        
        ------------
        fonction qui initialise les atributs de l'objet
        ------------
        """
        self.x = x
        self.y = y
        self.joueur = joueur
        self.carte_actuelle = carte
        self.monstre = pygame.image.load("images/fantome_noir.png").convert_alpha()

    def suivre_joueur(self):
        """
        pre :
            self = objet en cour d'instance
        post :
            /
        
        ------------
        fonction qui permet à l'ennemi de suivre le joueur
        ------------
        """
        
        deplacement_x = self.joueur.x - self.x
        deplacement_y = self.joueur.y - self.y
        distance = math.sqrt(deplacement_x**2 + deplacement_y**2) # Calculer la direction vers le joueur

        if distance <= 800:
            if distance != 0:
                deplacement_x /= distance #calcul la longeur du deplacement a faire (plutot la direction ici)
                deplacement_y /= distance

            self.x += deplacement_x*2# Déplacer l'ennemi vers le joueur a la vitesse 3.5
            self.y += deplacement_y*2
    
    def mouvement_continu(self):
        """
        pre :
            self = objet en cour d'instance
        post :
            /
        
        ------------
        fonction qui permet a l'ennemi de partir quand un joueur est caché
        ------------
        """
        new_x = self.x + 2.0
        self.x = new_x     
 
    def dessiner(self, fenetre,x,y):
        """
        pre :
            fenetre = fenetre sur laquelle il faut dessiner l'ennemi
            x = position de l'enemi sur l'axe des abscisse (int)
            y = position de l'enemi sur l'axe des ordonné (int)
        post :
            /

        ------------
        fonction qui dessine l'ennemi
        ------------
        """
        fenetre.blit(self.monstre, (x-40, y-50))#-40 et -50 pour centrer l'ennemi au centre de la position
        
