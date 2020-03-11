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


if __name__ == "__main__":
  affichage_titre(titre)
  affichage_aire_de_jeu(40, 100, "SNAKE")
  curses.napms(10000)
  curses.endwin()


def controle(win, key, keys = [____]):
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
	old_key = curses.KEY_SAVE

	# Aquisition d'un nouveau caractère depuis le clavier
	key = win.____

	# Si aucune touche actionnée (pas de nouveau caractère)
	# ou pas dans la liste des touches acceptées
	# key prend la valeur de la dernière touche connue
	if key == ____ or key not in ____ :
		key = ____

	# Raffaichissement de la fenètre
	win.refresh()

	# retourne le code la touche
	return ____

  
