import time
import curses

def affichage_titre(titre):
  for ligne in titre:
    print(ligne)
  
  time.sleep(2)


titre =['   _____       _   _                    _____             _        ',       
        '  |  __ \     | | | |                  / ____|           | |       ',
        '  | |__) |   _| |_| |__   ___  _ __   | (___  _ __   __ _| | _____ ',
        '  |  ___/ | | | __|  _ \ / _ \|  _ \   \___ \|  _ \ / _  | |/ / _ \ ',
        '  | |   | |_| | |_| | | | (_) | | | |  ____) | | | | (_| |   <  __/',
        '  |_|    \__, |\__|_| |_|\___/|_| |_| |_____/|_| |_|\__,_|_|\_\___|',
        '          __/ |                                                    ',
        '         |___/                                                     ']



def affichage_aire_de_jeu(hauteur, largeur, titre):
    curses.initscr()
    win = curses.newwin(hauteur, largeur, 0, 0)
    win.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    win.nodelay(1)
    win.box()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win.addstr(0, largeur//2 - len(titre)//2, titre, curses.color_pair(1))
    win.refresh()
    curses.beep()
    return win

def controle(win, key, keys = [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, 27]):
	'''
	Controles de jeu
	paramètres :
	  win : fenètre en cours
	  key : dernière touche reconnue
	  keys: liste des touches acceptées par défaut
	retour :
	  code de la touche reconnue
	'''
	old_key = key
	key = win.getch()
	if key == "" or key not in keys :
		key = old_key
	win.refresh()
	return key

def jeu(win):
	'''
	Moteur du jeu
	paramètre :
	  win : fenètre en cours
	retour :
	  score à la fin du jeu
	'''
	key = curses.KEY_RIGHT
	score = 0
	snake = [[4, 10], [4, 9], [4, 8]]
	food = [10, 20]
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	win.addch(food[0], food[1], chr(211), curses.color_pair(2))  
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
	for i in range(len(snake)):
		win.addstr(snake[i][0], snake[i][1], '*', curses.color_pair(3))
	curses.beep()
	while key!=27:
		key = controle(win, key)
	return score


if __name__ == "__main__":
  affichage_titre(titre)
  curses.initscr()
  curses.start_color()
  window = affichage_aire_de_jeu(20, 60, 'SNAKE')
  score = jeu(window)
  curses.endwin()

  print('\n\n\n')
  print(f'Votre score est de : {score}')
  print('\n\n\n')

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
		snake.insert(0, snake[0][0], snake[0][1]+1)

	# Sinon si on appui sur la flèche "à gauche",
	# la tête se déplace de 1 caractère vers la gauche (colonne - 1)
	elif key == KEY_LEFT:
		snake.insert(0, snake[0][0], snake[0][1]-1)

	# Sinon si on appui sur la flèche "en haut",
	# la tête se déplace de 1 caractère vers le haut (ligne - 1)
	elif key == KEY_UP:
		snake.insert(0, snake[0][0]-1, snake[0][1])

	# Sinon si on appui sur la flèche "en bas",
	# la tête se déplace de 1 caractère vers le bas (ligne + 1)
	elif key == KEY_DOWN:
		snake.insert(0, snake[0][0]+1, snake[0][1])

	# si la serpent arrive au bord de la fenêtre (20 lignes x 60 colonnes)
	if snake[0][0] == 0:
		 snake[0][0] = win.getmaxyx()[0]-1

	if snake[0][1] == 0:
		snake[0][1] = win.getmaxyx()[1]-1

	if snake[0][0] == win.getmaxyx()[0]-1:
		 snake[0][0] = 1

	if snake[0][1] == win.getmaxyx()[1]-1:
		snake[0][1] = 1


	# Suppression du dernier anneau du serpent.
	# Sera conditionner plus tard au fait que le serpent mange ou pas une pomme
	# Le score sera alors également mis à jour
	last = snake.pop()


	# Affichage de la tête à sa nouvelle position en bleu sur fond jaune
	win.addstr(snake[0][0], snake[0][1], curses.color_pair(3))

	# Effacement du dernier anneau : affichage du caractère "espace" sur fond noir
	win.addstr(last[0], last[1], ' ', curses.color_pair(1))

	# Affichage du score dans l'aire de jeu
	win.addstr(0, 2, 'Score : ' + str(score) + ' ')

	# Attendre avant le pas suivant
	vitesse = 1
	win.timeout(150//vitesse)

	# tuple contenant :
	# - la liste des positions en cours des anneaux du serpent
	# - score en cours
	return snake, score
