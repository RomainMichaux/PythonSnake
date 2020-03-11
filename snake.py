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
