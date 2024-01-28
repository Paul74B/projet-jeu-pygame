from os import chdir
from random import randint

structurecarte = []

chdir("./")
fichier = open("carte.txt",'r')
structure_carte = fichier.readlines()
fichier.close()

