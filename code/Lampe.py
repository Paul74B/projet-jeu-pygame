import pygame

class Lampe:
    def __init__(self):
        self.surface = pygame.image.load('images/lampe.webp').convert_alpha()

        
    def dessiner(self, surface, x, y):
        """
        pre :
            surface = fentre de jeu sur laquelle il faut afficher le personnage (str)
            x = position du personnage sur l'axe des abscisse (int)
            y = position du personnage sur l'axe des ordonnes (int)
        post :
            /

        ------------
        fonction qui dessine la lampe
        ------------
        """
        x -= int(self.surface.get_width()/2)
        y -= int(self.surface.get_height()/2)
        bg = surface.copy()
        bg.fill((0,0,0))
        bg.blit(self.surface, [x, y], None)
        surface.blit(bg, [0, 0], None, pygame.BLEND_MULT)
        
