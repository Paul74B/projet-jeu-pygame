import pygame
from code.Config import *
from code.Map import *


class Joueur:

    def __init__(self, x, y, carte):
        """
        pre :
            x = position du personnage en x sur la carte (int)
            y = position du personnage en y sur la carte (int)
            carte = carte sur laquel on joue en ce moment
         post :
            /
        
        ------------
        fonction qui defini les attributs de la classe joueur
        ------------
        """
        self.x = x
        self.y = y
        self.carte_actuelle = carte
        self.sprint_barre = 100  
        self.sprint_decrement = 2  
        self.avantstop = pygame.image.load("images/joueur/avantstop.png").convert_alpha()
        #avant marcher
        self.avant0 = pygame.image.load("images/joueur/avant/avant0.png").convert_alpha()
        self.avant1 = pygame.image.load("images/joueur/avant/avant1.png").convert_alpha()
        self.avant2 = pygame.image.load("images/joueur/avant/avant2.png").convert_alpha()
        self.avant3 = pygame.image.load("images/joueur/avant/avant3.png").convert_alpha()
        self.avant4 = pygame.image.load("images/joueur/avant/avant4.png").convert_alpha()
        self.avant5 = pygame.image.load("images/joueur/avant/avant5.png").convert_alpha()
        self.avant6 = pygame.image.load("images/joueur/avant/avant6.png").convert_alpha()
        self.avant7 = pygame.image.load("images/joueur/avant/avant7.png").convert_alpha()
        #arriere marcher
        self.arriere0 = pygame.image.load("images/joueur/arriere/arriere0.png").convert_alpha()
        self.arriere1 = pygame.image.load("images/joueur/arriere/arriere1.png").convert_alpha()
        self.arriere2 = pygame.image.load("images/joueur/arriere/arriere2.png").convert_alpha()
        self.arriere3 = pygame.image.load("images/joueur/arriere/arriere3.png").convert_alpha()
        self.arriere4 = pygame.image.load("images/joueur/arriere/arriere4.png").convert_alpha()
        self.arriere5 = pygame.image.load("images/joueur/arriere/arriere5.png").convert_alpha()
        self.arriere6 = pygame.image.load("images/joueur/arriere/arriere6.png").convert_alpha()
        self.arriere7 = pygame.image.load("images/joueur/arriere/arriere7.png").convert_alpha()
        #gauche marcher
        self.gauche0 = pygame.image.load("images/joueur/gauche/gauche0.png").convert_alpha()
        self.gauche1 = pygame.image.load("images/joueur/gauche/gauche1.png").convert_alpha()
        self.gauche2 = pygame.image.load("images/joueur/gauche/gauche2.png").convert_alpha()
        self.gauche3 = pygame.image.load("images/joueur/gauche/gauche3.png").convert_alpha()
        self.gauche4 = pygame.image.load("images/joueur/gauche/gauche4.png").convert_alpha()
        self.gauche5 = pygame.image.load("images/joueur/gauche/gauche5.png").convert_alpha()
        self.gauche6 = pygame.image.load("images/joueur/gauche/gauche6.png").convert_alpha()
        self.gauche7 = pygame.image.load("images/joueur/gauche/gauche7.png").convert_alpha()
        #droite marcher
        self.droite0 = pygame.image.load("images/joueur/droite/droite0.png").convert_alpha()
        self.droite1 = pygame.image.load("images/joueur/droite/droite1.png").convert_alpha()
        self.droite2 = pygame.image.load("images/joueur/droite/droite2.png").convert_alpha()
        self.droite3 = pygame.image.load("images/joueur/droite/droite3.png").convert_alpha()
        self.droite4 = pygame.image.load("images/joueur/droite/droite4.png").convert_alpha()
        self.droite5 = pygame.image.load("images/joueur/droite/droite5.png").convert_alpha()
        self.droite6 = pygame.image.load("images/joueur/droite/droite6.png").convert_alpha()
        self.droite7 = pygame.image.load("images/joueur/droite/droite7.png").convert_alpha()


    def mouvement(self, deplacement_x, deplacement_y):
        """
        pre :
            deplacement_x = deplacement du joueur dans une direction sur l'axe des abscices d'un nombre dx de pixels(droite = un nombre positifs et gauche un nombre negatif) (float)
            deplacement_y = deplacement du joueur sur l'axe des ordonnes d'un nombre dy de pixels (bas = nombre positif et haut = nombre negatif) (float)
         post :
            /
        
        ------------
        fonction qui gere le deplacement du joueur dans la carte, met a jour ce coordonées et accelere le deplacement si la touche shift pour le sprint est pressé
        ------------
        """
        self.x += deplacement_x // 1.5 #diviser par 1.5 pour ralentir la vitesse par rapport au sprint sur l'axe des abscisses
        self.y += deplacement_y // 1.5 #diviser par 1.5 pour ralentir la vitesse par rapport au sprint sur l'axe des ordonnes

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_q] or keys[pygame.K_d]) : 

            self.sprint_barre -= self.sprint_decrement #decremente l'argument print_barre de print_decrement
            if self.sprint_barre > 0 :
                self.x += deplacement_x // 1 #diviser par 1 pour accelerer la vitesse par rapport a la marche normal sur l'axe des abscisse
                self.y += deplacement_y // 1 #diviser par 1 pour accelerer la vitesse par rapport a la marche normal sur l'axe des ordonnes


        if self.sprint_barre < 100 :
                self.sprint_barre = self.sprint_barre + 1 #augmente la barre de sprint tant qu'elle est inferieur a 100 (augmente moins vite que reduit quand on sprint)
          

    def dessiner(self, fenetre, x, y, direction, image):
        """
        pre :
            fenetre = fentre de jeu sur laquelle il faut afficher le personnage (str)
            x = position du personnage sur l'axe des abscisse (int)
            y = position du personnage sur l'axe des ordonnes (int)
            direction = direction du personnage, si il va vers le haut, vers le bas, la gauche ou la droite (int)
            image = numero de l'image a laquelle on est rendu pour faire defiler l'image lorsque les personnage est en mouvement (int)
        
        post :
            /
        
        ------------
        fonction qui permet d'afficher le personnage a l'ecran et qui gere l'animation de quand celui ci marche
        ------------
        """
        if direction == 0:
            fenetre.blit(self.avantstop, (x, y))
        elif direction == 1 :
            if image == 0: #l'ensemble des if/elif permet de gerer l'animation pour que le personnage marche (pareil pour chaque direction)
                fenetre.blit(self.avant0, (x, y))
            elif image == 1:
                fenetre.blit(self.avant1, (x, y))
            elif image == 2:
                fenetre.blit(self.avant2, (x, y))
            elif image == 3:
                fenetre.blit(self.avant3, (x, y))
            elif image == 4:
                fenetre.blit(self.avant4, (x, y))
            elif image == 5:
                fenetre.blit(self.avant5, (x, y))
            elif image == 6:
                fenetre.blit(self.avant6, (x, y))
            elif image == 7:
                fenetre.blit(self.avant7, (x, y))
        elif direction == 2 :
            if image == 0:
                fenetre.blit(self.arriere0, (x, y))
            elif image == 1:
                fenetre.blit(self.arriere1, (x, y))
            elif image == 2:
                fenetre.blit(self.arriere2, (x, y))
            elif image == 3:
                fenetre.blit(self.arriere3, (x, y))
            elif image == 4:
                fenetre.blit(self.arriere4, (x, y))
            elif image == 5:
                fenetre.blit(self.arriere5, (x, y))
            elif image == 6:
                fenetre.blit(self.arriere6, (x, y))
            elif image == 7:
                fenetre.blit(self.arriere7, (x, y))
        elif direction == 3 :
            if image == 0:
                fenetre.blit(self.gauche0, (x, y))
            elif image == 1:
                fenetre.blit(self.gauche1, (x, y))
            elif image == 2:
                fenetre.blit(self.gauche2, (x, y))
            elif image == 3:
                fenetre.blit(self.gauche3, (x, y))
            elif image == 4:
                fenetre.blit(self.gauche4, (x, y))
            elif image == 5:
                fenetre.blit(self.gauche5, (x, y))
            elif image == 6:
                fenetre.blit(self.gauche6, (x, y))
            elif image == 7:
                fenetre.blit(self.gauche7, (x, y))
        elif direction == 4 :
            if image == 0:
                fenetre.blit(self.droite0, (x, y))
            elif image == 1:
                fenetre.blit(self.droite1, (x, y))
            elif image == 2:
                fenetre.blit(self.droite2, (x, y))
            elif image == 3:
                fenetre.blit(self.droite3, (x, y))
            elif image == 4:
                fenetre.blit(self.droite4, (x, y))
            elif image == 5:
                fenetre.blit(self.droite5, (x, y))
            elif image == 6:
                fenetre.blit(self.droite6, (x, y))
            elif image == 7:
                fenetre.blit(self.droite7, (x, y))
        pygame.draw.rect(fenetre, (0, 255, 0), (500, 50 - 10, self.sprint_barre * 3, 9))  # dessine la barre de sprint
        pygame.draw.rect(fenetre, (255, 0, 0), (500, 50, 100 * 3, 6))  # dessine le contour de la barre de sprint
    

    def verifier_collision_mur(self, deplacement_x, deplacement_y):
        """
        pre :
             deplacement_x = deplacement du joueur dans une direction sur l'axe des abscices d'un nombre dx de pixels(droite = un nombre positifs et gauche un nombre negatif) (float)
             deplacement_y = deplacement du joueur sur l'axe des ordonnes d'un nombre dy de pixels (bas = nombre positif et haut = nombre negatif) (float)
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre le mur et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 48 #definition de la hauteur du personnage (en réalité la moitié vue qu'on souhaite que le personnage puisse passer en partie au dessus du mur pour créer un effet 3d vue de haut)

        coin_sup_gauche_x = int(self.x + 4 + deplacement_x) #deplacé de 4 pour avoir un vrau effet de collision et pas juste un bout de la main
        coin_sup_gauche_y = int(self.y +25 + deplacement_y) #le haut est decalle de 25 (vers le bas) pour donner l'impression expliqué au dessus

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme - 8
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme - 32

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "#": #verifie qu'on ne rencontre pas un mur
                    return True  # Collision avec un mur

        return False  # Aucune collision avec un mur


    def verifier_collision_cle(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la cle et le personnage
        ------------

        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y)

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "K": 
                    return True  # Collision

        return False  # Aucune collision

    def verifier_collision_porteA(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la porteA et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y)

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme 
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "A": 
                    return True  # Collision

        return False  # Aucune collision
    
    def verifier_collision_porteB(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la porteB et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y)

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme 
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "B": 
                    return True  # Collision

        return False  # Aucune collision
    
    def verifier_collision_porteC(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la porteC et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y) 

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme 
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "C": 
                    return True  # Collision

        return False  # Aucune collision

    def verifier_collision_cachette(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la cachette et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y) 

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme 
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "H": 
                    return True  # Collision

        return False  # Aucune collision
    
    def verifier_collision_porteF(self):
        """
        pre :
            /
        post :
            return True si il y a une collision et False sinon
        
        ------------
        fonction qui verifie si il y a une collisions entre la porte F(pour fin du jeu) et le personnage
        ------------
        """
        largeur_bonhomme = 25 #definition de la largeur du personnage 
        hauteur_bonhomme = 60 #definition de la hauteur du personnage 

        coin_sup_gauche_x = int(self.x)
        coin_sup_gauche_y = int(self.y) 

        coin_inf_droit_x = coin_sup_gauche_x + largeur_bonhomme 
        coin_inf_droit_y = coin_sup_gauche_y + hauteur_bonhomme

        coins_bonhomme = [(coin_sup_gauche_x, coin_sup_gauche_y),(coin_inf_droit_x, coin_sup_gauche_y),(coin_sup_gauche_x, coin_inf_droit_y),(coin_inf_droit_x, coin_inf_droit_y)] #definition de tuple de coordonné pour les 4 coins des colisions

        for coin_x, coin_y in coins_bonhomme:
            map_x = int(coin_x) // 30 #verifie les coordonne dans la carte, hors une case fait 30 pixel de large donc pour revenir a la carte nous devons diviser par 30 pour trouver les coordonnes dans la carte
            map_y = int(coin_y) // 30

            if self.carte_actuelle[map_y][map_x] == "F": 
                    return True  # Collision

        return False  # Aucune collision