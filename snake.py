import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import time
from random import randint


def affichage_titre(titre):
    for ligne in titre:
        print(ligne)
    time.sleep(2)

def beep_fin():
    for i in range(10):
        curses.beep()


def affichage_aire_de_jeu(hauteur, largeur, titre):
    win = curses.newwin(hauteur, largeur, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.nodelay(1)
    win.box()

    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    win.addstr(0, 27, titre, curses.color_pair(2))
    win.refresh()
    curses.beep()
    return win

def controle(win, key, keys = [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, 27]):

	# Sauvegarde de la dernière touche reconnue
	old_key = key

	# Aquisition d'un nouveau caractère depuis le clavier
	key = win.getch()

	# Si aucune touche actionnée (pas de nouveau caractère)
	# ou pas dans la liste des touches acceptées
	# key prend la valeur de la dernière touche connue
	if key == "" or key not in keys :
		key = old_key

	# Raffaichissement de la fenètre
	win.refresh()

	# retourne le code la touche
	return key


def jeu(win):
	'''
	Moteur du jeu
	paramètre :
	  win : fenètre en cours
	retour :
	  score à la fin du jeu
	'''

	# initialisation du jeu
	# Le serpent se dirige vers la droite au début du jeu.
	# C'est comme si le joueur avait utilisé la flèche droite au clavier
	key = KEY_RIGHT
	score = 0

	# Definition des coordonnées du serpent
	# Le serpent est une liste de d'anneaux composées de leurs coordonnées ligne, colonne
	# La tête du serpent est en 4,10, l'anneau 1 en 4,9, le 2 en 4,8
	snake = [[4, 10], [4, 9], [4, 8]]

	# La nouriture (pomme) se trouve en 10,20
	food = [10, 20]

	# Affichage la nouriture en vert sur fond noir dans la fenêtre
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	win.addch(food[0], food[1], chr(211), curses.color_pair(2))  # Prints the food

	# Affichage du serpent en bleu sur fond jaune
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
	# sur toute la longeur du serpent
	for i in range(len(snake)):
		# affichage de chaque anneau dans la fenêtre en ligne, colonne
		win.addstr(snake[i][0], snake[i][1], '*', curses.color_pair(3))

	# Emission d'un beep  au début du jeu
	curses.beep()
	end = False
  
	# Tant que le joueur n'a pas quitter le jeu
	while key != 27 and not end:

		key = controle(win, key)
		snake, score = deplacement(win, score, key, snake, food)
		end = perdu(win, snake)
	return score

		




def deplacement(win, score, key, snake, food):
	'''
	Déplacements du serpent
	paramètres :
	  win : fenètre en cours
	  score : score en cours
	  key : touche de controle en cours
	  snake : liste des positions en cours des anneaux du serpent
	  food : liste de la position de la pomme
	retourne :
	  tuple contenant la liste des positions en cours des anneaux du serpent et score en cours
	'''
	# Si on appui sur la flèche "à droite",
	# la tête se déplace de 1 caractère vers la droite (colonne + 1)
	if key == KEY_RIGHT:
		snake.insert(0, [snake[0][0], snake[0][1]+1])

	# Sinon si on appui sur la flèche "à gauche",
	# la tête se déplace de 1 caractère vers la gauche (colonne - 1)
	elif key == KEY_LEFT:
		snake.insert(0, [snake[0][0], snake[0][1]-1])

	# Sinon si on appui sur la flèche "en haut",
	# la tête se déplace de 1 caractère vers le haut (ligne - 1)
	elif key == KEY_UP:
		snake.insert(0, [snake[0][0]-1, snake[0][1]])

	# Sinon si on appui sur la flèche "en bas",
	# la tête se déplace de 1 caractère vers le bas (ligne + 1)
	elif key == KEY_DOWN:
		snake.insert(0, [snake[0][0]+1, snake[0][1]])

	# si la serpent arrive au bord de la fenêtre (20 lignes x 60 colonnes)
	if snake[0][0] == 0:
		snake[0][0] = win.getmaxyx()[0]-2

	if snake[0][1] == 0:
		snake[0][1] = win.getmaxyx()[1]-2

	if snake[0][0] == win.getmaxyx()[0]-1:
	  snake[0][0] = 1

	if snake[0][1] == win.getmaxyx()[1]-1:
	  snake[0][1] = 1


	# Suppression du dernier anneau du serpent.
	# Sera conditionner plus tard au fait que le serpent mange ou pas une pomme
	# Le score sera alors également mis à jour
	food, snake, last, score = mange_pomme(win, food, snake, score)


	# Affichage de la tête à sa nouvelle position en bleu sur fond jaune
	win.addstr(snake[0][0], snake[0][1], '*', curses.color_pair(3))

	# Effacement du dernier anneau : affichage du caractère "espace" sur fond noir
	win.addstr(last[0], last[1], ' ', curses.color_pair(1))

	# Affichage du score dans l'aire de jeu
	win.addstr(0, 2, 'Score : ' + str(snake[0][0]) + ' ')

	# Attendre avant le pas suivant
	vitesse = plus_vite(score)
	win.timeout(150//vitesse)

	# tuple contenant :
	# - la liste des positions en cours des anneaux du serpent
	# - score en cours
	return snake, score

def mange_pomme(win, food, snake, score):
	'''
	Le serpent a-t-il mangé la pomme ?
	paramètres :
	  win : fenètre en cours
	  food : liste des coordonnées de la pomme
	  snake : liste des coordonnées des anneaux du serpent
	  score : score en cours
	retour :
	  Tuple constitué de :
	    - la liste des coordonnées actualisées de la pomme,
	    - la liste des coordonnées du serpent,
	    - la liste des coordonnées du dernier anneau à supprimer
	    - le score en cours
	'''
	# initialisation de la liste contenant les coordonnées du dernier anneau du serpent
	last = [0,0]

	# Si le serpent a mangé la pomme
	if snake[0] == food:
		# Emettre un beep
		curses.beep()

		# incrémenter le score
		score += 1

		# Réactualiser les coordonnées de la pomme
		# On recommence tant que les coordonnées de la pomme sont dans le serpent
		while food in snake:

			# On actualise au hasard les coordonnées de la pomme
			# dans les limite de la fenêtre
			# voir la documentation de la fonction window.getmaxyx()
			food[0] = randint(1, win.getmaxyx()[0]-2)
			food[1] = randint(1, win.getmaxyx()[1]-2)

		# Affichage de la pomme aux nouvelles coordonnées en vert sur fond noir
		win.addch(food[0], food[1], chr(211), curses.color_pair(2))
		win.refresh()

	# Sinon
	else:
		# Suppression du dernier anneau du serpent
		last = snake.pop()

	return food, snake, last, score

def perdu(win, snake):
	'''
	Le serpent se mange-t-il la queue ?
	paramètre :
	  win : fenètre en cours
	  snake : liste des positions en cours des anneaux du serpent
	retourne :
	  True si on perd, False sinon
	'''

	# initialisation de la variable end à retourner
	end = False

	# Si la tête du serpent est dans le corps
	if snake[0] in snake[1:] :

		# Afiicher "GAME OVER !" en blanc sur fond rouge au milieu de la fenêtre
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
		win.addstr(win.getmaxyx()[0]//2, win.getmaxyx()[1]//2-5, "GAME OVER !", curses.color_pair(4))
		win.refresh()

		# Emission d'une série de beep.
		# Vous devrez écrire vous-même cette fonction !
		beep_fin()

		# On laisse 2 secondes au joueur pour s'assurer
		# qu'il ait bien compris qu'il a perdu !
		curses.napms(2000)
		end = True
	return end


def plus_vite(score):
	'''
	Calcul de la vitesse du serpent
	paramètre :
	  score : score en cours
	retourne :
	  vitesse du serpent entre 1 et 10
	'''

	# vitesse est le quotient de la division entière de score par 5 ( + 1)
	vitesse = score // 5 + 1

	# Si vitesse est superieur à 10, alors vitesse = 10
	if vitesse > 10:
		vitesse = 10

	return vitesse

titre = ['  _______     _________ _    _  ____  _   _    _____ _   _          _  ________ ',
         ' |  __ \ \   / |__   __| |  | |/ __ \| \ | |  / ____| \ | |   /\   | |/ |  ____|',
         ' | |__) \ \_/ /   | |  | |__| | |  | |  \| | | (___ |  \| |  /  \  |   /| |__   ',
         ' |  ___/ \   /    | |  |  __  | |  | | . ` |  \___ \| . ` | / /\ \ |  < |  __|  ',
         ' | |      | |     | |  | |  | | |__| | |\  |  ____) | |\  |/ ____ \| . \| |____ ',
         ' |_|      |_|     |_|  |_|  |_|\____/|_| \_| |_____/|_| \_/_/    \_|_|\_|______|']

affichage_titre(titre)
curses.initscr()
curses.start_color()
window = affichage_aire_de_jeu(20, 60, 'SNAKE')
score = jeu(window)
curses.endwin()

print('\n\n\n')
print(f'Votre score est de : {score}')
print('\n\n\n')
