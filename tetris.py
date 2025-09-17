#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "votre nom"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "votre nom"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "votre nom"
__email__ = "votre email"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys

import constantes
from constantes import PIECES
from constantes import COULEURS
from constantes import VITESSE
from constantes import HAUTEUR_APPARITION_PIECES
from constantes import NB_LIGNES_POUR_TETRIS
from constantes import NB_LIGNES_POUR_NIVEAU
from constantes import TAILLE_FONT_DEFAUT
from constantes import TAILLE_FONT_TITRE
from constantes import HAUTEUR_POSITION_TEXTE_SCORE

TAILLE_PLATEAU = tuple([constantes.DIM_PLATEAU[i]*constantes.TAILLE_BLOC[i] for i in range(2)])
TAILLE_PLABORD = tuple([constantes.DIM_PLATEAU[i]*constantes.TAILLE_BLOC[i]+constantes.BORDURE_PLATEAU*2 for i in range(2)])

MARGE = tuple([constantes.TAILLE_FENETRE[i]-TAILLE_PLATEAU[i]- constantes.BORDURE_PLATEAU*2 for i in range(2)])
START_PLATEAU = int(MARGE[0]/2), MARGE[1]+2*constantes.BORDURE_PLATEAU
START_PLABORD = int(MARGE[0]/2)-constantes.BORDURE_PLATEAU, MARGE[1]+constantes.BORDURE_PLATEAU

CENTRE_FENETRE = tuple([constantes.TAILLE_FENETRE[i]/2 for i in range(2)])
POS = CENTRE_FENETRE[0], CENTRE_FENETRE[1]+100
POSITION_SCORE = constantes.TAILLE_FENETRE[0] - START_PLABORD[0] / 2, HAUTEUR_POSITION_TEXTE_SCORE
POSITION_PIECES = POSITION_SCORE[0], HAUTEUR_POSITION_TEXTE_SCORE + 30
POSITION_LIGNES = POSITION_SCORE[0], HAUTEUR_POSITION_TEXTE_SCORE + 60
POSITION_TETRIS = POSITION_SCORE[0], HAUTEUR_POSITION_TEXTE_SCORE + 90
POSITION_NIVEAU = POSITION_SCORE[0], HAUTEUR_POSITION_TEXTE_SCORE + 120

for name, rotations in PIECES.items():
	PIECES[name] = [[[int(i) for i in pixel] for pixel in rotation.splitlines()] for rotation in rotations]

PIECES_KEYS = list(PIECES.keys())

# Classe Tetris
class Jeu:
	"""
		Une classe modélisant un jeu de Tetris

		Exemples
		--------
		Pour lancer le jeu de Tetris :
			jeu = Jeu()
			print("Jeu prêt")
			jeu.start()
			print("Partie démarée")
			jeu.play()
			print("Partie terminée")
			jeu.stop()
			print("Arrêt du programme")
	"""
	def __init__(self):
		"""
			Le constructeur de la classe Jeu
		"""
		pygame.init()
		self.clock = pygame.time.Clock()
		self.surface = pygame.display.set_mode(constantes.TAILLE_FENETRE)
		self.fonts = {
			'defaut': pygame.font.Font('freesansbold.ttf', TAILLE_FONT_DEFAUT),
			'titre': pygame.font.Font('freesansbold.ttf', TAILLE_FONT_TITRE),
		}
		pygame.display.set_caption('Application Tetris')

	def start(self)->None:
		"""
			Méthode affichant l'écran d'accueil
		"""
		self._afficher_texte('Tetris', CENTRE_FENETRE, font = 'titre')
		self._afficher_texte('Appuyer sur une touche...', POS)
		self._attente()

	def stop(self)->None:
		"""Méthode affichant le message de défaite
		"""
		self._afficher_texte('Perdu', CENTRE_FENETRE, font='titre')
		self._attente()
		self._quitter()

	def _afficher_texte(self, text:str, position:tuple, couleur:int=9, font:str='defaut')-> None:
		"""Méthode permettant d'afficher le texte passé en paramètre avec la position, la couleur et la font

		Args:
			text (str): le texte à afficher
			position (tuple): la position du texte
			couleur (int, optional): La couleur du texte. Defaults to 9.
			font (str, optional): La font du texte. Defaults to 'defaut'.
		"""
		font = self.fonts.get(font, self.fonts['defaut'])
		couleur=COULEURS.get(couleur, COULEURS[9])
		rendu = font.render(text, True, couleur)
		rect = rendu.get_rect()
		rect.center = position
		self.surface.blit(rendu, rect)
	def _get_event(self)-> int:
		"""Gère les évènements, renvoie une touche si elle a été appuyée

		Returns:
			int: la touche qui a été appuyée
		"""
		for event in pygame.event.get():
			if event.type == QUIT:
				self._quitter()
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					self._quitter()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continue
				return event.key
				
	def _quitter(self)->None:
		"""Quitte le jeu
		"""
		print("Quitter")
		pygame.quit()
		sys.exit()
	def _rendre(self)->None:
		"""Met à jour l'affichage et fait avancer l'horloge
		"""
		pygame.display.update()
		self.clock.tick()
	def _attente(self)-> None:
		"""Met le jeu en pause
		"""
		print("Attente")
		while self._get_event() == None:
			self._rendre()
	def _get_piece(self)->list[str]:
		"""Choisit aléatoirement une pièce

		Returns:
			list[str]: Une pièce aléatoirement sélectionnée
		"""
		return PIECES.get(random.choice(PIECES_KEYS))
	def _get_current_piece_color(self)-> int:
		"""Renvoie la couleur de la pièce actuelle

		Returns:
			int: le numéro de la couleur de la pièce actuelle
		"""
		for ligne in self.current[0]:
			for couleur in ligne:
				if couleur != 0:
					return couleur
		return 0
	def _calculer_donnees_piece_courante(self)->None:
		"""Calcule les coordonées de la pièce actuelle
		"""
		rep_piece=self.current[self.position[2]]
		coords = []
		for num_ligne, ligne in enumerate(rep_piece):
			for num_pixel, pixel in enumerate(ligne):
				if pixel != 0:
					coords.append([num_ligne+self.position[0], num_pixel+self.position[1]])
		self.coordonnees = coords
	def _est_valide(self, x:int=0, y:int=0, r:int=0) -> bool:
		"""Renvoie True si la pièce actuelle décalée selon les paramètres donnés ne dépasse pas du plateau, False sinon

		Args:
			x (int, optional): Le décalage de la pièce en x. Defaults to 0.
			y (int, optional): Le décalage de la pièce en y. Defaults to 0.
			r (int, optional): Le numéro de la rotation de la pièce. Defaults to 0.

		Returns:
			bool: True si la pièce est bien placée selon les décalages, False sinon
		"""
		max_x, max_y = constantes.DIM_PLATEAU
		if r == 0: # si la pièce n'a pas été tournée
			coordonnees = self.coordonnees
		else:
			rep_piece=self.current[(self.position[2]+r)%len(self.current)]
			coords = []
			for num_ligne, ligne in enumerate(rep_piece):
				for num_pixel, pixel in enumerate(ligne):
					if pixel != 0:
						coords.append([num_ligne+self.position[0], num_pixel+self.position[1]])
			coordonnees = coords
#			print("Rotation testée: %s" % coordonnees)
		for coord_x, coord_y in coordonnees:
			if not 0 <= x + coord_x < max_x:
#				print("Non valide en X: cx=%s, x=%s" % (cx, x))
				return False
			elif coord_y <0:
				continue
			elif y + coord_y >= max_y:
#				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
				return False
			else:
				if self.plateau[coord_y+y][coord_x+x] != 0:
#					print("Position occupée sur le plateau")
					return False
#		print("Position testée valide: x=%s, y=%s" % (x, y))
		return True
	def _poser_piece(self)->None:
		"""Dépose une pièce sur le plateau et met à jour les paramètres associés : le nombre de lignes complétées, le score, le niveau, le tetris 
		"""
		print(self.coordonnees)
		print("La pièce est posée")
		if self.position[1] <= 0:
			self.perdu = True
		# Ajout de la pièce parmi le plateau
		couleur = self._get_current_piece_color()
		for coord_x, coord_y in self.coordonnees:
			self.plateau[coord_y][coord_x] = couleur
		completees = []
		# calculer les lignes complétées
		for i, line in enumerate(self.plateau[::-1]):
			for case in line:
				if case == 0:
					break
			else:
				print(self.plateau)
				print(">>> %s" % (constantes.DIM_PLATEAU[1]-1-i))
				completees.append(constantes.DIM_PLATEAU[1]-1-i)
		lignes = len(completees)
		for ligne_completee in completees:
			self.plateau.pop(ligne_completee)
		for i in range(lignes):
			self.plateau.insert(0, [0] * constantes.DIM_PLATEAU[0])
		# calculer le score et autre
		self.lignes += lignes
		self.score += lignes * self.niveau
		self.niveau = int(self.lignes / NB_LIGNES_POUR_NIVEAU) + 1
		if lignes >= NB_LIGNES_POUR_TETRIS:
			self.tetris +=1
			self.score += self.niveau * self.tetris
		# Travail avec la pièce courante terminé
		self.current = None
	def _first(self)->None:
		"""Initialise le plateau et les valeurs
		"""
		self.plateau = [[0] * constantes.DIM_PLATEAU[0] for i in range(constantes.DIM_PLATEAU[1])]
		self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
		self.current, self.next, self.perdu = None, self._get_piece(), False
	def _next(self)-> None:
		"""Choisit et prépare la pièce suivante, la positionne sur le plateau
		"""
		print("Piece suivante")
		self.current, self.next = self.next, self._get_piece()
		self.pieces += 1
		self.position = [int(constantes.DIM_PLATEAU[0] / 2)-2, HAUTEUR_APPARITION_PIECES, 0]
		self._calculer_donnees_piece_courante()
		self.dernier_mouvement = self.derniere_chute = time.time()
		print(self.current)
		print(self.position)
		print(self.coordonnees)
	def _gerer_evenements(self)-> None:
		"""Gère les évènements
		"""
		event = self._get_event()
		if event == K_p:
			print("Pause")
			self.surface.fill(COULEURS.get(0))
			self._afficher_texte('Pause', CENTRE_FENETRE, font='titre')
			self._afficher_texte('Appuyer sur une touche...', POS)
			self._attente()
		elif event == K_LEFT:
			print("Mouvement vers la gauche")
			if self._est_valide(x=-1):
				self.position[0] -= 1
		elif event == K_RIGHT:
			print("Mouvement vers la droite")
			if self._est_valide(x=1):
				self.position[0] += 1
		elif event == K_DOWN:
			print("Mouvement vers le bas")
			if self._est_valide(y=1):
				self.position[1] += 1
		elif event == K_UP:
			print("Mouvement de rotation")
			if self._est_valide(r=1):
				self.position[2] = (self.position[2] + 1) %len(self.current)
		elif event == K_SPACE:
			print("Mouvement de chute %s / %s" % (self.position, self.coordonnees))
			if self.position[1] <=0:
				self.position[1] = 1
				self._calculer_donnees_piece_courante()
			hauteur_de_chute = 0
			while self._est_valide(y=hauteur_de_chute):
				hauteur_de_chute+=1
			self.position[1] += hauteur_de_chute-1
		self._calculer_donnees_piece_courante()
	def _gerer_gravite(self)->None:
		"""Fait tomber la pièce sur le plateau
		"""
		if time.time() - self.derniere_chute > VITESSE:
			self.derniere_chute = time.time()
			if not self._est_valide():
				print ("On est dans une position invalide")
				self.position[1] -= 1
				self._calculer_donnees_piece_courante()
				self._poser_piece()
			elif self._est_valide() and not self._est_valide(y=1):
				self._calculer_donnees_piece_courante()
				self._poser_piece()
			else:
				print("On déplace vers le bas")
				self.position[1] += 1
				self._calculer_donnees_piece_courante()
	def _dessiner_plateau(self)->None:
		"""Dessine le plateau et les pièces posées dessus
		"""
		self.surface.fill(COULEURS.get(0))
		pygame.draw.rect(self.surface, COULEURS[8], START_PLABORD+TAILLE_PLABORD, constantes.BORDURE_PLATEAU)
		for num_ligne, ligne in enumerate(self.plateau):
			for num_case, case in enumerate(ligne):
				couleur = COULEURS[case]
				position = num_case, num_ligne
				coordonnees = tuple([START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)
		if self.current is not None:
			for position in self.coordonnees:
				couleur = COULEURS.get(self._get_current_piece_color())
				coordonnees = tuple([START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)
		self.score, self.pieces, self.lignes, self.tetris, self.niveau#TODO
		self._afficher_texte('Score: >%s' % self.score, POSITION_SCORE)
		self._afficher_texte('Pièces: %s' % self.pieces, POSITION_PIECES)
		self._afficher_texte('Lignes: %s' % self.lignes, POSITION_LIGNES)
		self._afficher_texte('Tetris: %s' % self.tetris, POSITION_TETRIS)
		self._afficher_texte('Niveau: %s' % self.niveau, POSITION_NIVEAU)

		self._rendre()
	def play(self)->None:
		"""Lance le jeu
		"""
		print("Jouer")
		self.surface.fill(COULEURS.get(0))
		self._first()
		while not self.perdu:
			if self.current is None:
				self._next()
			self._gerer_evenements()
			self._gerer_gravite()
			self._dessiner_plateau()

if __name__ == '__main__':
	jeu = Jeu()
	print("Jeu prêt")
	jeu.start()
	print("Partie démarée")
	jeu.play()
	print("Partie terminée")
	jeu.stop()
	print("Arrêt du programme")

