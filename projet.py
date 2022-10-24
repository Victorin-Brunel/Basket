#########################################
# Jeu de Basketball                     #
# Fait par Adam IZEM et Victorin BRUNEL #
# Nom du fichier : Basket.py            #
# Date : Octobre 2022                   #
#########################################

from random import uniform, randint, choice

class Match :
  def __init__(self) :

    print("  _______   ________   ______   ___   ___   ______   _________   _______   ________   __       __          ")
    print("/_______/\ /_______/\ /_____/\ /___/\/__/\ /_____/\ /________/\/_______/\ /_______/\ /_/\     /_/\         ")
    print("\::: _  \ \\\::: _  \ \\\::::_\/_\::.\ \\\ \ \\\::::_\/_\__.::.__\/\::: _  \ \\\::: _  \ \\\:\ \    \:\ \        ")
    print(" \::(_)  \/_\::(_)  \ \\\:\/___/\\\:: \/_) \ \\\:\/___/\  \::\ \   \::(_)  \/_\::(_)  \ \\\:\ \    \:\ \       ")
    print("  \::  _  \ \\\:: __  \ \\\_::._\:\\\:. __  ( ( \::___\/_  \::\ \   \::  _  \ \\\:: __  \ \\\:\ \____\:\ \____  ")
    print("   \::(_)  \ \\\:.\ \  \ \ /____\:\\\: \ )  \ \ \:\____/\  \::\ \   \::(_)  \ \\\:.\ \  \ \\\:\/___/\\\:\/___/\ ")
    print("    \_______\/ \__\/\__\/ \_____\/ \__\/\__\/  \_____\/   \__\/    \_______\/ \__\/\__\/ \_____\/ \_____\/ ")
    input(" " * 47 + "[Press Enter]" + " "*47)

    self.nbActionsMax = int(input("Combien d'actions voulez vous dans ce match ? : "))
    self.equipes = []
    for i in range (1, 3):
      print("> Création de l'équipe " + str(i) + " : ")
      self.equipes.append(Equipe(input("Nom de l'équipe : ")))
      self.equipes[-1].createJoueurs()
    self.eqActive = 0
    input("Pressez entrer pour lancer la partie")
    print('-' * 30)
    self.lancerJeu()
    
  def lancerJeu(self): # Méthode qui permet de lancer le jeu
    etat = "Normal" # Permet de définir le type d'action en jeu (normal, meneur (boost accordé) ou pivot (la balle reste au meme joueur))
    
    while self.nbActionsMax != 0: # Boucle de jeu
      eqAttaque = self.equipes[self.eqActive]
      eqDefense = self.equipes[1 - self.eqActive]
      
      if etat != "Pivot": # Chgt du joueur en attaque ssi pivot n'a pas pris le rebond
        a = eqAttaque.getJoueurActif()
        while a == eqAttaque.getJoueurActif():
            i = randint(0,4)
            a = eqAttaque.getJoueur(i)
        eqAttaque.setJoueurActif(a)
        
      b = eqDefense.getJoueurActif()
      while b == eqDefense.getJoueurActif():
        i = randint(0,4)
        b = eqDefense.getJoueur(i)
      eqDefense.setJoueurActif(b)

      c = eqDefense.joueurActif.contrer()
      jActif = eqAttaque.getJoueurActif()
      a = 0
      
      while a not in ["1", "2", "3"] :
        print("> " + jActif.getNom() + " de l'équipe " + eqAttaque.getNomEquipe() + " a la balle ! Voici ses caractéristiques  : ")
        print('---')
        jActif.affCaracteristiques()
        print('---')
        print("> Il fait face à " + eqDefense.joueurActif.getNom() + " qui a pour caractéristiques : ")
        print('---')
        eqDefense.joueurActif.affCaracteristiques()
        print('---')
        print("Boost du meneur sur la caractéristique " + boost[1] + " : " + str(round(boost[0], 2)) if etat == "Meneur" else "")
        a = input("> Tapez 1 pour shooter; \n> Taper 2 pour passer; \n> Tapez 3 pour faire un double pas; \nVotre choix : ")
        print('-' * 30)
        if a not in ["1", "2", "3"]:
            print("Veuillez réessayer")

      if a == "1" : # Shoot
        s = jActif.shooter()
        if etat == "Meneur" and boost[1] == "shoot":
            s*= boost[0]
            
        if s > uniform(0, c + s):
          eqAttaque.addScore(2)
          if jActif.poste.getNom() == "Arriere" and jActif.poste.troisPts():
            eqAttaque.addScore(1) 
            print("> L'equipe " + eqAttaque.getNomEquipe() + " a marqué 3 points !!")
          else:
            print("> L'equipe " + eqAttaque.getNomEquipe() + " a marqué 2 points !!")
          print("> Score : " + eqAttaque.getNomEquipe() + " : " + str(eqAttaque.getScore()) + " | " + eqDefense.getNomEquipe() + " : " +str(eqDefense.getScore()))
        else :
          print("> " + str(jActif.getNom() + " s'est fait contré !! Balle à l'adversaire"))
        etat = "Normal"
        self.eqActive = 1 - self.eqActive
      
      elif a == "2": # Passe
        p = jActif.passer()
        if etat == "Meneur" and boost[1] == "passe":
            p *= boost[0]
            
        if p > uniform(0, c + p):
          etat = "Normal"
          print("> Passe réussie")
          if jActif.poste.getNom() == "Meneur":
            boost = jActif.poste.getBoost()
            etat = 'Meneur'
            print("> Le meneur accorde son boost à son coéquipier sur la caractéristique " + boost[1] + " avec un effet multiplicateur de X" + str(round(boost[0], 2)))
        else:
            print("> Passe ratée ! Balle à l'adversaire")
            etat = "Normal"
            self.eqActive = 1 - self.eqActive

      else: # Double pas
        d = jActif.doublePas()
        if etat == "Meneur" and boost[1] == "doublePas":
            d *= boost[0]
        
        if d > uniform(0, c + d) :
          eqAttaque.addScore(2)
          print ("> L'equipe " + eqAttaque.getNomEquipe() + " a marqué 2 points !!")
          print("> Score : " + eqAttaque.getNomEquipe() + " : " + str(eqAttaque.getScore()) + " | " + eqDefense.getNomEquipe() + " : " +str(eqDefense.getScore()))
          etat = "Normal"
          self.eqActive = 1 - self.eqActive
        else :
          print("> " + str(jActif.getNom() + " s'est fait contré !!"))
          if jActif.poste.getNom() == "Pivot" and jActif.poste.prendreRebond():
            etat = "Pivot"
            print("> Le joueur prend le rebond et garde la balle ! ")
          else:
            print("> Balle à l'adversaire")
            etat = "Normal"
            self.eqActive = 1 - self.eqActive

      input("> Pressez entrer")
      print("-" * 30)
          
      self.nbActionsMax = self.nbActionsMax - 1 
    print("Fin du jeu !")
    print("Score final : " + eqAttaque.getNomEquipe() + " : " + str(eqAttaque.getScore()) + " | " + eqDefense.getNomEquipe() + " : " +str(eqDefense.getScore()))
    print(((eqAttaque.getNomEquipe() if eqAttaque.getScore() > eqDefense.getScore() else eqDefense.getNomEquipe()) + " a gagné !") if eqAttaque.getScore() != eqDefense.getScore() else "Egalité")

    print('-'*30)
    print("Merci d'avoir joué à notre jeu, nous espérons que celui ci vous a plu ! ")
    print("Victorin BRUNEL et Adam IZEM")

class Equipe:
  def __init__(self, nom: str):
    self.nom = nom
    self.score = 0
    self.joueurs = []
    self.joueurActif = None

  def getNomEquipe(self):
    return self.nom

  def getJoueurActif(self):
    return self.joueurActif

  def getJoueur(self, i):
    return self.joueurs[i]

  def addScore(self, score):
    self.score += score

  def getScore(self):
    return self.score
    
  def setJoueurActif(self, j):
    self.joueurActif = j

  def createJoueurs(self):
    postes = {"Meneur" : Meneur(), "Pivot" : Pivot(), "Ailier 1" : Ailier(), "Ailier 2" : Ailier(), "Arriere" : Arriere()} # Initialisation des postes
    
    for i in range(5): # Creation des joueurs
      self.joueurs.append(Joueur(input('Nom du joueur ' + str(i + 1) + ' : ')))
    print("-"*30 + "\n" + "> Voici vos joueurs et leurs caractéristiques : ")
    for elt in self.joueurs: # Affichage des joueurs
      elt.affCaracteristiques()
      print('--')
    input("Pressez entrer")

    j = self.joueurs.copy()
    print("> Assignation des postes : ")
    for key in postes:
      cond = True
      while cond:
        for elt in j: # Affichage des joueurs restant
          elt.affCaracteristiques()
          print('--')
        postes[key].getCaracteristiques()
        nom = input("Entrez le nom du joueur : ") # Assignation d'un joueur à un poste
        for i in range(len(j)):
          if j[i].getNom() == nom:
            j[i].setPoste(postes[key])
            cond = False 
            j.pop(i)
            break
        if cond:
          print("> Veulliez réessayer")
      input("Pressez entrer")
    print("> Voici vos joueurs et leurs caractéristiques : ")
    for elt in self.joueurs:
      elt.affCaracteristiques()
      print('--')
    print("-"*30)
  
class Joueur:
  def __init__(self, nom: str):
    self.nom = nom
    self.doPas = uniform(0.3, 0.49)
    self.passe = uniform(0.3, 0.49)
    self.shoot = uniform(0.3, 0.49)
    self.contre = uniform(0, 0.3)
    self.poste = None

  def getNom(self):
    return self.nom

  def setPoste(self, poste):
    self.poste = poste

  def shooter(self):
    return self.shoot * (self.poste.getShoot() if self.poste != None else 1)

  def doublePas(self):
    return self.doPas * (self.poste.getDoublePas() if self.poste != None else 1)

  def passer(self):
    return self.passe * (self.poste.getPasse() if self.poste != None else 1)

  def contrer(self):
    return self.contre * (self.poste.getContre() if self.poste != None else 1)

  def affCaracteristiques(self):
    print(self.nom)
    print(self.poste.getNom() if self.poste != None else '')
    print("   Passe : " + str(round(self.passer(), 2)) + (" (" + str(round(self.passe, 2)) + " X " + str(round(self.poste.getPasse(), 2)) + ')' if self.poste != None else ''))
    print("   Contre : " + str(round(self.contrer(), 2)) + (" (" + str(round(self.contre, 2)) + " X " + str(round(self.poste.getContre(), 2))+ ')' if self.poste != None else ''))
    print("   Double pas : " + str(round(self.doublePas(), 2)) + (" (" + str(round(self.doPas, 2)) + " X " + str(round(self.poste.getDoublePas(), 2)) + ')' if self.poste != None else ''))
    print("   Shoot : " + str(round(self.shooter(), 2)) + (" (" + str(round(self.shoot, 2)) + " X " + str(round(self.poste.getShoot(), 2)) + ')' if self.poste != None else ''))    

class Poste :
  def __init__(self) :
    self.doublePas = 1
    self.shoot = 1
    self.contre = 1
    self.passe = 1

  def getCaracteristiques(self) :
    print ("> " + self.nom + ' (' + "Double pas : X " + str(self.doublePas) + " ; Shoot : X " + str(self.shoot) + " ; Contre : X " + str(self.contre) + " ; Passe : X " + str(self.passe) + ")")
    
  def getDoublePas(self) :
    return self.doublePas

  def getShoot(self) :
    return self.shoot

  def getContre(self) :
    return self.contre

  def getPasse(self) :
    return self.passe

  def getNom(self):
    return self.nom

class Ailier(Poste) :
  def __init__(self) :
    super().__init__()
    self.nom = "Ailier"
    self.doublePas = 1.5
    self.shoot = 1.5
    self.passe = 1.5
    self.contre = 1.5

class Meneur(Poste) :
  def __init__(self) :
    super().__init__()
    self.nom = "Meneur"
    self.doublePas = 1.7
    self.shoot = 1.7
    self.passe = 1.9
    self.contre = 0.5
  
  def getBoost(self):
      return [uniform(1, 1.5), choice(["doublePas", "shoot", "passe"])]
    
class Pivot(Poste):
  def __init__(self):
    super().__init__()
    self.nom = "Pivot"
    self.doublePas = 1.9
    self.contre = 1.9
    self.shoot = 0.5
    self.rebond = 0.25

  def prendreRebond(self):
    return self.rebond > uniform(0, 1)
  
class Arriere(Poste):
  def __init__(self):
    super().__init__()
    self.nom = "Arriere"
    self.shoot = 1.9
    self.tpts = 0.5

  def troisPts(self):
    a = uniform(0, 1)
    return a < self.tpts
    
a = Match()