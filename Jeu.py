import pygame
import sys

import code.Joueur as Joueur
import code.Ennemi as Ennemi
import code.Lampe as Lampe
from code.Config import *
from code.Map import *
from code.Map2 import *
from code.Map3 import *
from code.Map4 import *

import math
import time
from random import randint
from moviepy.editor import *



pygame.init()

class Jeu:
    def __init__(self):
        """
        pre :
            /
        post :
            /
        
        ------------
        methode qui initie tous les attributs de la class jeu
        ------------
        """
        pygame.display.set_caption("Backroom 2.0")

        self.image_effrayante = pygame.image.load("images/game_over.png")
        self.image_effrayante = pygame.transform.scale(self.image_effrayante, (1920, 1080))
        self.image_trappe = pygame.image.load("images/labyrinthe/trappe.png")
        self.image_cle = pygame.image.load("images/labyrinthe/cle.png")
        self.sol = pygame.image.load("images/labyrinthe/sol.png").convert()
        self.cachette = pygame.image.load("images/labyrinthe/cachette.png").convert()
        self.mur = pygame.image.load("images/labyrinthe/mur.png").convert()
        
        self.video_debut = VideoFileClip('video/debut.mp4')
        self.video_fin = VideoFileClip('video/fin.mp4')

        # Initialiser la clock
        self.clock = pygame.time.Clock()

        # Définir le nombre de FPS souhaité
        self.fps = 30        

        self.font = pygame.freetype.Font("polices/WreckedShip.ttf", 35)
        self.font_pause = pygame.freetype.Font("polices/WreckedShip.ttf", 20)
        self.font_cle = pygame.freetype.Font("polices/Curse of the Zombie.ttf", 50)

        self.joueur = Joueur.Joueur(130, 130, structure_carte)

        self.ennemis = [Ennemi.Ennemi(1500, 500, self.joueur, structure_carte),
                        Ennemi.Ennemi(2000, 3000, self.joueur, structure_carte),
                        Ennemi.Ennemi(3000, 3000, self.joueur, structure_carte),
                        Ennemi.Ennemi(4000, 5000, self.joueur, structure_carte),
                        Ennemi.Ennemi(6000, 7000, self.joueur, structure_carte),
                        Ennemi.Ennemi(1000, 5000, self.joueur, structure_carte),]
        
        
        self.lamp = Lampe.Lampe()

        self.camera_x, self.camera_y = 0, 0
        self.image = 0
        self.direction = 0

        self.largeur_carte = len(structure_carte[0]) * 30
        self.hauteur_carte = len(structure_carte) * 30

        
    def boucle_principale(self):
        """
        pre :
            /
        post :
            /
        
        ------------
        fonction principal du jeu
        ------------
        """
        self.video_debut.preview() #video de generique debut
        
        os.environ['SDL_VIDEO_CENTERED'] = '1' # Permet de centrer le fenètre du jeu au milieu de l'écran après la vidéo
        self.fenetre = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0) #initie la fenetre d'origine
        
        pygame.mixer.music.load("sons/musique_peur.mp3")
        pygame.mixer.music.play(-1)
        
        self.son_effrayant = pygame.mixer.Sound("sons/scream.mp3")
        self.son_ambiance = pygame.mixer.Sound("sons/Backrooms entity sound effect.mp3")
        self.porte_son = pygame.mixer.Sound("sons/son porte.mp3")
        self.cle_son = pygame.mixer.Sound("sons/son cle.mp3")
        self.marche_son = pygame.mixer.Sound("sons/marche.mp3")
        self.marche_son.set_volume(0.2)
        self.course_son = pygame.mixer.Sound("sons/cours.mp3")
        self.course_son.set_volume(0.3)
        self.son_suivi = pygame.mixer.Sound("sons/cri.mp3")
        self.son_suivi.set_volume(0.1)
        
        #variable mutiples necessaire pour la suite du programme remis a 0 en chaque debut de partie
        running = True
        game_over = False
        pause = False
        cachette = False
        temps_sortie_cachette = 0
        self.cle = 0
        

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        pause = self.pause(pause) #bouton espace pour mettre le jeu en pause
                    
                    if event.key == pygame.K_e :
                        if self.joueur.verifier_collision_cachette() : #verifie le colisions avec la cachette
                            if not cachette:
                                cachette = True 
                                temps_sortie_cachette = pygame.time.get_ticks() + 2000  # 2000 millisecondes (2 secondes)
                            elif cachette and pygame.time.get_ticks() >= temps_sortie_cachette:
                                cachette = False
                        else:
                            self.touche_e()#sinon appelle la fonction qui verifie tout les cas si la touche e est pressé

            keys = pygame.key.get_pressed()
            deplacement_x, deplacement_y = 0, 0
            self.direction = 0
            deplacement_x, deplacement_y = self.deplacement_joueur(keys, deplacement_x, deplacement_y)#deplacement du joueur

            if keys[pygame.K_ESCAPE]:
                quit() #bouton echappe pour quitter le jeu

            if not self.joueur.verifier_collision_mur(deplacement_x, deplacement_y) and cachette == False :
                self.joueur.mouvement(deplacement_x, deplacement_y)#verifier les collisions du joueur avec le mur
                
            
            for ennemi in self.ennemis:
                distance_joueur_ennemi = math.sqrt((self.joueur.x - ennemi.x)**2 + (self.joueur.y - ennemi.y)**2)
                if cachette and distance_joueur_ennemi < 1100 :
                    ennemi.mouvement_continu() #si il est dans une cachette alors l'ennemi pars
                    self.son_suivi.stop()
                else :
                    ennemi.suivre_joueur() #l'ennemi suis le joueur si il n'est pas dans une cachette
                    if distance_joueur_ennemi >= 500 and distance_joueur_ennemi <= 800:
                        self.son_suivi.play()
                    else :
                        self.son_suivi.stop()
                        

                        
                if distance_joueur_ennemi < 50:#si l'ennemi attrape le joueur alors c'est perdu, on lance alors game over
                    game_over = True
                    self.course_son.stop()
                    self.marche_son.stop()

            self.DRAW(cachette) #la fonction pour tout afficher
            
            if game_over:
                self.son_effrayant.play()
                self.screamer()


            pygame.display.update()
            pygame.display.flip()
            
            self.clock.tick(self.fps)

    def pause(self, pause):
        """
        pre :
            pause : est ce que le menu pause est accepté (bool)
        post :
            /
        
        ------------
        fonction qui affiche et gere le menu pause 
        ------------
        """
        self.fenetre.fill(BLACK)
        pause = True
        self.font.render_to(self.fenetre, (350, 450), "Jeu en Pause", RED)#affiche les informations
        self.font.render_to(self.fenetre, (160, 500), "Appuyez sur ESPACE pour reprendre", RED)#affiche les informations
        pygame.draw.rect(self.fenetre, WHITE, pygame.Rect(300, 800, 300, 50))
        self.font_pause.render_to(self.fenetre, (300, 820), "Retourner au menu principal", RED)#affiche les informations
        pygame.display.update()
        pygame.display.flip()
        while pause:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 300 <= x <= 600 and 800 <= y <= 850:#renvoie au menu si le bouton est cliqué
                            menu = Menu(1620, 1080, "Backroom 2.0")
                            menu.menu_principal()
                    if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        pause = False
                        pygame.event.clear() 
                        return pause #recomence le jeu si on appuie sur espace

    def touche_e(self):
        """
        pre :
            /
        post :
            /

        ------------
        fonction qui verifie tout les cas si la touche e est presse (des collisions) et applique alors ce qu'il faut faire
        ------------
        """
        if self.joueur.verifier_collision_cle():
            self.cle += 1 #ajoute une clé
            self.cle_son.play() #joue le son cle
            for y, ligne in enumerate(self.joueur.carte_actuelle):
                for x, case in enumerate(ligne):
                    if case == "K":
                        self.joueur.carte_actuelle[y] = self.joueur.carte_actuelle[y][:x] + " " + self.joueur.carte_actuelle[y][x+1:] #retire la cle de la carte en la changeant par du vide

        if self.joueur.verifier_collision_porteA() and self.cle == 1 and self.joueur.carte_actuelle == structure_carte: #permet de rentrer dans le niveau 1 si on a la cle (le programme se repetent pour toutes les portes donc meme chose mais avec niveau different)
            self.porte_son.play() #joue le son d'ouverture de la porte
            self.joueur = Joueur.Joueur(100, 20, structure_carte2)#change la carte du joueur 
            self.ennemis = [Ennemi.Ennemi(700, 800, self.joueur, structure_carte2)]#ajoute un ennemi dans le niveau
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte2
        if self.joueur.verifier_collision_porteA() and self.cle == 2 and self.joueur.carte_actuelle == structure_carte2 :
            self.porte_son.play()
            self.joueur.carte_actuelle = structure_carte
            self.ennemis = [
                Ennemi.Ennemi(700, 1000, self.joueur, structure_carte)
                            ]
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte
        if self.joueur.verifier_collision_porteB() and self.cle == 2 and self.joueur.carte_actuelle == structure_carte:
            self.porte_son.play()
            self.joueur = Joueur.Joueur(200, 50, structure_carte3)
            self.ennemis = [
                Ennemi.Ennemi(700, 700, self.joueur, structure_carte3)
                ]
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte3
        if self.joueur.verifier_collision_porteB() and self.cle == 3 and self.joueur.carte_actuelle == structure_carte3 :
            self.porte_son.play()
            self.joueur.carte_actuelle = structure_carte
            self.ennemis = [
                Ennemi.Ennemi(700, 1000, self.joueur, structure_carte)
                ]
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte
        if self.joueur.verifier_collision_porteC() and self.cle == 3 and self.joueur.carte_actuelle == structure_carte:
            self.porte_son.play()
            self.joueur = Joueur.Joueur(100, 50, structure_carte4)
            self.ennemis = [
                Ennemi.Ennemi(700, 800, self.joueur, structure_carte4)
                ]
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte4
        if self.joueur.verifier_collision_porteC() and self.cle == 4 and self.joueur.carte_actuelle == structure_carte4 :
            self.porte_son.play()
            self.joueur.carte_actuelle = structure_carte
            self.ennemis = [
                Ennemi.Ennemi(700, 1000, self.joueur, structure_carte)
                ]
            for ennemi in self.ennemis :
                ennemi.carte_actuelle = structure_carte             
        if self.joueur.verifier_collision_porteF() and self.cle >= 4 and self.joueur.carte_actuelle == structure_carte:
            self.video_fin.preview()
            menu = Menu(1620, 1080, "Backroom 2.0")
            menu.menu_principal()

    def deplacement_joueur(self, keys, deplacement_x, deplacement_y):
        """
        pre :
            deplacement_x = deplacement du joueur dans une direction sur l'axe des abscices d'un nombre dx de pixels(droite = un nombre positifs et gauche un nombre negatif) (float)
            deplacement_y = deplacement du joueur sur l'axe des ordonnes d'un nombre dy de pixels (bas = nombre positif et haut = nombre negatif) (float)
         post :
            deplacement_x = deplacement du joueur dans une direction sur l'axe des abscices d'un nombre dx de pixels(droite = un nombre positifs et gauche un nombre negatif) (float)
            deplacement_y = deplacement du joueur sur l'axe des ordonnes d'un nombre dy de pixels (bas = nombre positif et haut = nombre negatif) (float)
        
        
        ------------
        fonction qui gere le deplacement du joueur dans la carte en appelant la methode mouvement, ainsi que joue le son du deplacement
        ------------
        """
        if keys[pygame.K_q]:
            deplacement_x = -5 #q = gauche donc negatif
            self.direction = 3 #regle la bonne direction
            if pygame.mixer.get_busy() == False:
                if keys[pygame.K_LSHIFT]: #joue le son courir si shift est presse sinon marche
                    self.marche_son.stop()
                    self.course_son.play()
                else:
                    self.course_son.stop()
                    self.marche_son.play()
        if keys[pygame.K_d]:
            deplacement_x = 5#d = droite donc positif
            self.direction = 4
            if pygame.mixer.get_busy() == False:
                if keys[pygame.K_LSHIFT]:
                    self.marche_son.stop()
                    self.course_son.play()
                else:
                    self.course_son.stop()
                    self.marche_son.play()
        if keys[pygame.K_z]:
            deplacement_y = -5#z = haut donc negatif
            self.direction = 2
            if pygame.mixer.get_busy() == False:
                if keys[pygame.K_LSHIFT]:
                    self.marche_son.stop()
                    self.course_son.play()
                else:
                    self.course_son.stop()
                    self.marche_son.play()
        if keys[pygame.K_s]:
            deplacement_y = 5#s = bas donc positif
            self.direction = 1
            if pygame.mixer.get_busy() == False:
                if keys[pygame.K_LSHIFT]:
                    self.marche_son.stop()
                    self.course_son.play()
                else:
                    self.course_son.stop()
                    self.marche_son.play()

        if deplacement_x == 0 and deplacement_y == 0 : #si il est imobile on coupe le son de marche et course
                self.marche_son.stop()
                self.course_son.stop()
        return deplacement_x, deplacement_y

    def screamer(self):
        """
        pre :
            /
        post :
            /
        
        ------------
        fonction qui gere la mort du personnage et le renvoie au menu principal
        ------------
        """
        
        self.fenetre = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.fenetre.fill((0, 0, 0))
        self.fenetre.blit(self.image_effrayante, (0, 0))#screamer image
        pygame.display.update()
        pygame.display.flip()
        time.sleep(2) #attend un petit peu
        menu = Menu(1620, 1080, "Backroom 2.0")
        menu.menu_principal() #retour au menu principal

    def DRAW(self, cachette):
        """
        pre :
            cachette = savoir si le personnage est ou pas dans sa cachette (bool)
        post :
            /
        
        -------------
        fonction qui affiche tout ce qu'il faut afficher a l'ecran
        ------------
        """
        self.camera_x = self.joueur.x - WIDTH // 2#regle la taille de la camera pour se reperer dans l'image et pour centrer le joueur dans l'ecran 
        self.camera_y = self.joueur.y - HEIGHT // 2

        joueur_x_affiche = self.joueur.x - self.camera_x#regle les coordones du joueur dans l'image
        joueur_y_affiche = self.joueur.y - self.camera_y
        self.fenetre.fill(BLACK) #fond noir
        for y, ligne in enumerate(self.joueur.carte_actuelle):
            for x, case in enumerate(ligne):
                if case == "#":
                    self.fenetre.blit(self.mur, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30)) #si c'est un #, placer un mur
                elif case == " ":
                        self.fenetre.blit(self.sol, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30))#placer un sol si c'est un espace
                elif case == "K":
                    self.fenetre.blit(self.sol, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30))
                    self.fenetre.blit(self.image_cle, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30)) #placer une cle et en dessous un sol
                elif case == "A":
                    self.fenetre.blit(self.image_trappe, (x * 30 - self.camera_x, y * 30 - self.camera_y, 60, 60))#place ules portes a chaque fois 
                elif case == "B":
                    self.fenetre.blit(self.image_trappe, (x * 30 - self.camera_x, y * 30 - self.camera_y))
                elif case == "C":
                    self.fenetre.blit(self.image_trappe, (x * 30 - self.camera_x, y * 30 - self.camera_y))
                elif case == "H":
                    self.fenetre.blit(self.cachette, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30)) #place la cachette
                elif case == "F":
                    self.fenetre.blit(self.image_trappe, (x * 30 - self.camera_x, y * 30 - self.camera_y, 30, 30))



        
        for ennemi in self.ennemis:
            ennemi.dessiner(self.fenetre, ennemi.x - self.camera_x, ennemi.y - self.camera_y) #dessiner les ennemis
            
        self.lamp.dessiner(self.fenetre, joueur_x_affiche, joueur_y_affiche) #dessiner la lampe = rond noir autour du joueur
        
        if self.image == 7 : #animation du joueur
            self.image = 0
        else :
            self.image+=1

        self.joueur.dessiner(self.fenetre, joueur_x_affiche, joueur_y_affiche,self.direction, self.image) #affichage du joueur
        
        #affichage de tous les textes dans chaque situation 
        if not self.joueur.verifier_collision_cle() and not self.joueur.verifier_collision_porteA() and not self.joueur.verifier_collision_porteB() and not self.joueur.verifier_collision_porteC() and not self.joueur.verifier_collision_cachette() and not self.joueur.verifier_collision_porteF():
            texte = "CLES = " + str(self.cle)
            self.font_cle.render_to(self.fenetre, (70, 45), texte, RED)
            pygame.display.update()
            pygame.display.flip()
            
        if self.joueur.verifier_collision_cachette():
            if cachette == False :
                self.font.render_to(self.fenetre, (210, 80), "Appuyez sur E pour vous caché", RED)
                pygame.display.update()
                pygame.display.flip()
            else :
                self.font.render_to(self.fenetre, (330, 80), "Vous êtes caché", RED)
                                
        if self.joueur.verifier_collision_cle():
            self.font.render_to(self.fenetre, (220, 80), "Appuyez sur E pour récuperer", RED)
            pygame.display.update()
            pygame.display.flip()
        
        if self.joueur.verifier_collision_porteA():
            if self.cle < 1:
                self.font.render_to(self.fenetre, (250, 80), "Une Clé est manquante", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 1 and self.joueur.carte_actuelle == structure_carte:
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 1 and self.joueur.carte_actuelle == structure_carte2:
                self.font.render_to(self.fenetre, (335, 80), "Trouve la clé", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 2 and self.joueur.carte_actuelle == structure_carte2 :   
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle > 1 and self.joueur.carte_actuelle == structure_carte:
                self.font.render_to(self.fenetre, (230, 80), "il n'y a plus rien à voir ici", RED)
                pygame.display.update()
                pygame.display.flip()
            
        if self.joueur.verifier_collision_porteB() :
            if self.cle < 2 :
                self.font.render_to(self.fenetre, (230, 80), "Cette porte semble fermee", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 2 and self.joueur.carte_actuelle == structure_carte :   
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 2 and self.joueur.carte_actuelle == structure_carte3 :   
                self.font.render_to(self.fenetre, (335, 80), "Trouve la clé", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 3 and self.joueur.carte_actuelle == structure_carte3 :   
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle > 2 and self.joueur.carte_actuelle == structure_carte :
                self.font.render_to(self.fenetre, (230, 80), "il n'y a plus rien à voir ici", RED)
                pygame.display.update()
                pygame.display.flip()

        if self.joueur.verifier_collision_porteC() :
            if self.cle < 3 :
                self.font.render_to(self.fenetre, (230, 80), "Cette porte semble fermee", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 3 and self.joueur.carte_actuelle == structure_carte :   
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 3 and self.joueur.carte_actuelle == structure_carte4 :   
                self.font.render_to(self.fenetre, (335, 80), "Trouve la clé", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle == 4 and self.joueur.carte_actuelle == structure_carte4 :   
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()
            if self.cle > 3 and self.joueur.carte_actuelle == structure_carte :
                self.font.render_to(self.fenetre, (230, 80), "il n'y a plus rien à voir ici", RED)
                pygame.display.update()
                pygame.display.flip()
                
        if self.joueur.verifier_collision_porteF() :
            if self.cle >= 4 :
                self.font.render_to(self.fenetre, (230, 80), "Appuyez sur E pour ouvrir", RED)
                pygame.display.update()
                pygame.display.flip()

        


####################################################################################################################################################
################################################### MENU PRINCIPAL #################################################################################
####################################################################################################################################################


class Menu:   
    
    """
    Classe représentant le menu principal du jeu.

    Attribues:
        - largeur (int): Largeur de la fenêtre du menu.
        - hauteur (int): Hauteur de la fenêtre du menu.
        - titre (str): Titre du menu.

    Methodes:
        - __init__(self, largeur, hauteur, titre): Initialisation de la classe Menu.
        - afficher_texte(self, texte, couleur, x, y, font=None): Affiche du texte sur la fenêtre.
        - afficher_texte1(self, texte, couleur, x, y, font=None): Affiche un autre style de texte sur la fenêtre.
        - afficher_titre(self): Affiche le titre du menu.
        - est_survole(self, rect, pos_souris): Vérifie si la souris survole un rectangle.
        - menu_principal(self): Gère le menu principal du jeu.
        - menu_parametres(self): Gère le menu des paramètres du jeu.
        - menu_credits(self): Gère le menu des crédits du jeu.
        - lancer_jeu(self): Lance le jeu en créant une instance de la classe Jeu et appelant sa boucle principale.
    """

    def __init__(self, largeur, hauteur, titre):
        
        """
        Initialise une instance de la classe Menu.

        pre:
            - largeur (int): Largeur de la fenêtre du menu.
            - hauteur (int): Hauteur de la fenêtre du menu.
            - titre (str): Titre du menu.
            
        Return :
            None
        """
        
        # Assignation des paramètres d'initialisation aux attributs de la classe
        self.largeur = largeur
        self.hauteur = hauteur
        
        # Création de la fenêtre avec la taille spécifiée et mode plein écran
        self.fenetre = pygame.display.set_mode((largeur, hauteur),pygame.FULLSCREEN)
        
        # Définition du titre de la fenêtre
        pygame.display.set_caption("Menu Backroom 2.0")

        # Assignation du titre du menu
        self.titre = titre

        # Définition des couleurs utilisées dans le menu
        self.blanc = (255, 255, 255)
        self.noir = (0, 0, 0)
        self.rouge_normal = (224, 209, 0)
        self.rouge_survole = (200, 0, 0)
        
        # Chargement de l'image d'overlay et de la musique du menu
        self.image_overlay = pygame.image.load('images/overlay.png').convert_alpha()
        pygame.mixer.music.load("sons/menu_son.mp3")
        pygame.mixer.music.play(-1)
        
        self.video_debut = VideoFileClip('video/debut.mp4')
        self.video_fin = VideoFileClip('video/fin.mp4')

        # Initialisation des polices de texte avec les fichiers de police spécifiés
        pygame.freetype.init()
        self.font_titre = pygame.freetype.Font("polices/police.ttf", 200)
        self.font = pygame.freetype.Font("polices/WreckedShip.ttf", 35)
        self.font_nombre = pygame.freetype.Font("polices/Curse of the Zombie.ttf", 30)
        
        # Chargement des chemins des images du menu et redimensionnement
        self.image_1 = [
        "images/Image menu/back18.png",
        "images/Image menu/back17.png",
        "images/Image menu/back16.png",
        "images/Image menu/back15.png",
        "images/Image menu/back14.png",
        "images/Image menu/back13.png",
        "images/Image menu/back12.png",
        "images/Image menu/back11.png",
        "images/Image menu/back10.png",
        "images/Image menu/back9.png",
        "images/Image menu/back8.png",
        "images/Image menu/back7.png",
        "images/Image menu/back6.png",
        "images/Image menu/back5.png",
        "images/Image menu/back4.png",
        "images/Image menu/back3.png",
        "images/Image menu/back2.png",
        "images/Image menu/back1.png",        
        ]
        
        # Boucle pour redimensionner chaque image et les stocker dans image_2
        self.image_2 = []
        for image in self.image_1 :
            img = pygame.image.load(image)
            image = pygame.transform.scale(img, (self.largeur, self.hauteur))
            self.image_2.append(image)
              
    
    def afficher_texte(self, texte, couleur, x, y, font=None):
        
        """
        Affiche du texte sur la fenêtre du menu.

        pre:
            - texte (str): Texte à afficher.
            - couleur (tuple): Couleur du texte au format (R, G, B).
            - x (int): Coordonnée x du coin supérieur gauche du texte.
            - y (int): Coordonnée y du coin supérieur gauche du texte.
            - font (pygame.freetype.Font, optional): Police de caractères à utiliser. Par défaut, la police par défaut de la classe Menu.

        post:
            None
        """
        
        # Sélection de la police de caractères spécifiée ou utilisation de la police par défaut
        font = font or self.font
        
        # Rendu du texte sur la fenêtre du menu aux coordonnées spécifiées
        font.render_to(self.fenetre, (x, y), texte, couleur)

    def afficher_texte1(self, texte, couleur, x, y, font=None):
        
        """
        Affiche un autre style de texte sur la fenêtre du menu.

        pre:
            - texte (str): Texte à afficher.
            - couleur (tuple): Couleur du texte au format (R, G, B).
            - x (int): Coordonnée x du coin supérieur gauche du texte.
            - y (int): Coordonnée y du coin supérieur gauche du texte.
            - font (pygame.freetype.Font, optional): Police de caractères à utiliser. Par défaut, la police par défaut de la classe Menu.

        post:
            None
        """
        
        # Sélection de la police de caractères spécifiée ou utilisation de la police par défaut
        font = self.font_nombre
        
        # Rendu du texte sur la fenêtre du menu aux coordonnées spécifiées
        font.render_to(self.fenetre, (x, y), texte, couleur)
        
    def afficher_titre(self):
        
        """
        Affiche le titre du menu sur la fenêtre.

        pre:
            None

        post:
            None
        """
        # Affiche le texte désiré en utilisant la méthode afficher_texte
        self.afficher_texte(self.titre, self.noir, self.largeur//5 , 100, font=self.font_titre)

    def est_survole(self, rect, pos_souris):
        
        """
        Vérifie si la souris survole un rectangle spécifié.

        pre:
        - rect (pygame.Rect): Rectangle à vérifier.
        - pos_souris (tuple): Position de la souris au format (x, y).

        post:
        bool: True si la souris survole le rectangle, False sinon.
        """
        
        # Utilise la méthode collidepoint de pygame.Rect pour vérifier la position de la souris
        return rect.collidepoint(pos_souris)
    

    def menu_principal(self):
        
        """
        Gère le menu principal du jeu.

        pre:
            None

        post:
            None
        """
        
        while True:
            
            # Remplit la fenêtre avec la couleur blanche
            self.fenetre.fill(self.blanc)
            
            # Affiche les images en boucle avec un effet de transition
            for img in self.image_2:
                self.fenetre.blit(img, ((0, 0)))
                time.sleep(0.12)
                self.fenetre.blit(self.image_overlay,(0, 0))
                
                # Gestion des événements pygame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 625 <= x <= 945 and 400 <= y <= 450:
                            self.lancer_jeu() # Lance le jeu
                            return
                        elif 625 <= x <= 945 and 500 <= y <= 550:
                            self.menu_parametres()  # Appeler la fonction du menu des paramètres
                        elif 625 <= x <= 945 and 600 <= y <= 650:
                            self.menu_credits() # Appeler la fonction du menu des credits
                        elif 625 <= x <= 945 and 700 <= y <= 750:
                            pygame.quit()
                            sys.exit() # Quitter le jeu
                            
                # Affiche le titre du menu
                self.afficher_titre()

                # Dessine les rectangles des boutons et les textes correspondants
                pygame.draw.rect(self.fenetre, self.noir, pygame.Rect(self.largeur//3 + 83, 398, 324, 54),2, 3)
                pygame.draw.rect(self.fenetre, self.noir, (self.largeur//3 + 83, 498, 324, 54),2, 3)
                pygame.draw.rect(self.fenetre, self.noir, (self.largeur//3 + 83, 598, 324, 54),2, 3)
                pygame.draw.rect(self.fenetre, self.noir, (self.largeur//3 + 83, 698, 324, 54),2, 3)            
                for bouton_rect, texte in [((self.largeur//3 + 85, 400, 320, 50), "Jouer"),
                                        ((self.largeur//3 + 85, 500, 320, 50), "Paramètres"),
                                        ((self.largeur//3 + 85, 600, 320, 50), "Crédits"),
                                        ((self.largeur//3 + 85, 700, 320, 50), "Quitter")]:
                    pygame.draw.rect(self.fenetre, self.noir, bouton_rect)
                    if self.est_survole(pygame.Rect(bouton_rect), pygame.mouse.get_pos()):
                        pygame.draw.rect(self.fenetre, self.rouge_survole, bouton_rect)
                        self.afficher_texte(texte, self.noir, bouton_rect[0] + 40, bouton_rect[1] + 15)
                    else:
                        pygame.draw.rect(self.fenetre, self.rouge_normal, bouton_rect)
                        self.afficher_texte(texte, self.noir, bouton_rect[0] + 50, bouton_rect[1] + 15)
                        
                # Met à jour l'affichage
                pygame.display.flip()

    def menu_parametres(self):
        
        """
        Gère le menu des paramètres du jeu.

        pre:
            None

        post:
            None
        """

        while True:
            
            # Remplit la fenêtre avec la couleur blanche
            self.fenetre.fill(self.blanc)
            
            # Affiche les images en boucle avec un effet de transition
            for img in self.image_2:
                self.fenetre.blit(img, ((0, 0)))
                time.sleep(0.12)
                self.fenetre.blit(self.image_overlay,(0, 0))
                
                # Gestion des événements pygame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 625 <= x <= 945 and 950 <= y <= 1000:
                            return  # Retourner au menu principal


                # Dessine le rectangle et affiche le titre du menu des paramètres
                pygame.draw.rect(self.fenetre, self.blanc, (self.largeur//3 + 80, 90, 340, 70))
                pygame.draw.rect(self.fenetre, self.rouge_normal, (self.largeur//3 + 85, 95, 330, 60))
                self.afficher_texte("Menu Paramètres", self.blanc, self.largeur//3 + 95, 110)

                # Afficher les paramètres de déplacement
                self.afficher_texte("Déplacements :", self.blanc, self.largeur//3, 200)
                self.afficher_texte("Avancer : Touche Z", self.noir, self.largeur//3, 250)
                self.afficher_texte("Reculer : Touche S", self.noir, self.largeur//3, 300)
                self.afficher_texte("Aller à gauche : Touche Q", self.noir, self.largeur//3, 350)
                self.afficher_texte("Aller à droite : Touche D", self.noir, self.largeur//3, 400)
                self.afficher_texte("Sprinter : Touche Shift gauche", self.noir, self.largeur//3, 450)

                # Afficher les paramètres d'interaction
                self.afficher_texte("Interaction :", self.blanc, self.largeur//3, 500)
                self.afficher_texte("Interagir : Touche E", self.noir, self.largeur//3, 550)

                # Afficher les paramètres du menu pause
                self.afficher_texte("Menu Pause :", self.blanc, self.largeur//3, 600)
                self.afficher_texte("Ouvrir le menu pause : Touche Espace (Space)", self.noir, self.largeur//3, 650)
                
                # Afficher les paramètres pour quitter le jeu
                self.afficher_texte("Quitter le jeu :", self.blanc, self.largeur//3, 700)
                self.afficher_texte("Fermer le jeu : Touche Echap (Escape)", self.noir, self.largeur//3, 750)
                
                
                # Dessine le rectangle et affiche le bouton de retour
                pygame.draw.rect(self.fenetre, self.blanc, (self.largeur//3 + 80, 945, 330, 60))
                for bouton_rect, texte in [((self.largeur//3 + 85, 950, 320, 50), "Retour")]:
                    pygame.draw.rect(self.fenetre, self.blanc, bouton_rect)
                    if self.est_survole(pygame.Rect(bouton_rect), pygame.mouse.get_pos()):
                        pygame.draw.rect(self.fenetre, self.rouge_survole, bouton_rect)
                        self.afficher_texte(texte, self.blanc, bouton_rect[0] + 40, bouton_rect[1] + 15)
                    else:
                        pygame.draw.rect(self.fenetre, self.rouge_normal, bouton_rect)
                        self.afficher_texte(texte, self.blanc, bouton_rect[0] + 50, bouton_rect[1] + 15)

                # Met à jour l'affichage
                pygame.display.flip()
            
    def menu_credits(self):
        
        """
        Gère le menu des crédits du jeu.

        pre:
            None

        post:
            None
        """

        while True:
            # Remplit la fenêtre avec la couleur blanche
            self.fenetre.fill(self.blanc)
            
            # Affiche les images en boucle avec un effet de transition
            for img in self.image_2:
                self.fenetre.blit(img, ((0, 0)))
                time.sleep(0.12)
                self.fenetre.blit(self.image_overlay,(0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 625 <= x <= 945 and 950 <= y <= 1000:
                            return  # Retourner au menu principal

                # Dessine le rectangle et affiche le titre du menu des credits
                pygame.draw.rect(self.fenetre, self.blanc, (self.largeur//3 + 80, 85, 330, 60))
                pygame.draw.rect(self.fenetre, self.rouge_normal, (self.largeur//3 + 85, 90, 320, 50))
                self.afficher_texte("Crédits", self.blanc, self.largeur//3 + 180, 100)
                
                # Copyright
                self.afficher_texte1("© 2023/2024 BACKDOOR CORP", self.blanc, self.largeur // 3, 150)

                # Développement
                self.afficher_texte("Développement :", self.blanc, self.largeur // 3, 200)
                self.afficher_texte("Lead Développeur : Paul & Marius", self.noir, self.largeur // 3, 250)
                self.afficher_texte("Programmeurs : Paul & Marius", self.noir, self.largeur // 3, 300)
                self.afficher_texte("Designers : Paul & Marius", self.noir, self.largeur // 3, 350)

                # Conception de jeu
                self.afficher_texte("Conception de jeu :", self.blanc, self.largeur // 3, 400)
                self.afficher_texte("Game Designer : Paul", self.noir, self.largeur // 3, 450)
                self.afficher_texte("Level Designers : Marius", self.noir, self.largeur // 3, 500)

                # Son et Musique
                self.afficher_texte("Son et Musique :", self.blanc, self.largeur // 3, 550)
                self.afficher_texte("Compositeur de la bande son : Youtube", self.noir, self.largeur // 3, 600)
                self.afficher_texte("Sound Designers : Marius", self.noir, self.largeur // 3, 650)
                self.afficher_texte("Cinématiques : Kane Pixels sur Youtube", self.noir, self.largeur // 3, 700)

                # Remerciements spéciaux
                self.afficher_texte("Remerciements spéciaux :", self.blanc, self.largeur // 3, 750)
                self.afficher_texte("À tous nos fans", self.noir, self.largeur // 3, 800)

                # Soutiens financiers
                self.afficher_texte("Soutiens financiers :", self.blanc, self.largeur // 3, 850)
                self.afficher_texte("Tout gratuit", self.noir, self.largeur // 3, 900)


                # Dessine le rectangle et affiche le bouton de retour
                pygame.draw.rect(self.fenetre, self.blanc, (self.largeur//3 + 80, 945, 330, 60))
                for bouton_rect, texte in [((self.largeur//3 + 85, 950, 320, 50), "Retour")]:
                    pygame.draw.rect(self.fenetre, self.blanc, bouton_rect)
                    if self.est_survole(pygame.Rect(bouton_rect), pygame.mouse.get_pos()):
                        pygame.draw.rect(self.fenetre, self.rouge_survole, bouton_rect)
                        self.afficher_texte(texte, self.blanc, bouton_rect[0] + 40, bouton_rect[1] + 15)
                    else:
                        pygame.draw.rect(self.fenetre, self.rouge_normal, bouton_rect)
                        self.afficher_texte(texte, self.blanc, bouton_rect[0] + 50, bouton_rect[1] + 15)

                # Met à jour l'affichage
                pygame.display.flip()

    def lancer_jeu(self):
        
        """
        Lance le jeu en créant une instance de la classe Jeu et en appelant sa boucle principale.

        pre:
        None

        post:
        None
        """

            # Lancer le jeu

        jeu = Jeu()
        jeu.boucle_principale()
        
    # Fin de la classe Menu
        

# Créer une instance du menu
menu = Menu(1620, 1080, "Backroom 2.0")

# Lancer le menu principal
menu.menu_principal()
