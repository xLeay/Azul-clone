from upemtk import *
from random import randint
import sys
from os.path import exists

def creer_matrice(n, debut=0, etape=0):
	"""
	CrÃ©e une matrice ayant n listes avec la chaÃ®ne grey rÃ©pÃ©tÃ©e plusieurs fois.

	>>> creer_matrice(5)
	[[], [], [], [], []]
	>>> creer_matrice(3, 1)
	[['grey'], ['grey'], ['grey']]
	>>> creer_matrice(3, 1, 1)
	[['grey'], ['grey', 'grey'], ['grey', 'grey', 'grey']]
	>>> creer_matrice(3, 1, 3/2)
	[['grey'], ['grey', 'grey'], ['grey', 'grey', 'grey', 'grey']]
	"""
	return [["grey"]*(debut+int(x*etape)) for x in range(n)]

def matrice_videe(M):
        """
        Retourne True si la matrice est vide, False sinon.
        
        >>> matrice_videe([[], [], []])
        True
        >>> matrice_videe([[], [], ['texte']])
        False
        """
        for el in M:
                if len(el) != 0:
                        return False
        return True

def liste_simple(plateaux):
        """
        Transforme une liste rÃ©cursive en liste simple

        >>> liste_simple([[[["aaa"]],"bbb"]])
        ['aaa', 'bbb']
        """
        L = []
        for el in plateaux:
                if type(el) is list:
                        L.extend(liste_simple(el))
                else:
                        L.append(el)
        return L

def banniere(txt, x, y):
	"""Affiche une banniÃ¨re ayant pour texte txt et ayant pour centre (x,y)."""
	rectangle(0,y-25,x*2,y+25,"grey","grey")
	texte(x,y,txt,"white","center","Arial")

def bouton(txt, x, y, zone, action, inter):
	"""Affiche un bouton ayant pour texte txt, pour centre (x,y) et pour interaction inter."""
	rectangle(x-50,y-20,x+50,y+20,"grey","grey")
	texte(x,y,txt,"white","center","Arial","14")
	zone.append([x-50,y-20,x+50,y+20])
	action.append(inter)

def demande_joueurs():
	"""
	Affiche l'Ã©cran demandant le nombre de joueurs et retourne
	2, 3 ou 4 en fonction du choix de l'utilisateur.
	"""
	rectangle(0,0,600,60,"black","black")
	texte(300,30,"Combien de joueurs ?","white","center","Arial")
	rectangle(0,60,200,200,"grey80","grey80")
	rectangle(200,60,400,200,"grey60","grey60")
	rectangle(400,60,600,200,"grey40","grey40")
	texte(100,130,"2","white","center","Arial")
	texte(300,130,"3","white","center","Arial")
	texte(500,130,"4","white","center","Arial")
	rectangle(0,200,600,260,"grey30","grey30")
	if exists("partie.sav"):
		texte(300,230,"Charger une partie prÃ©cÃ©dente","white","center","Arial")
	else:
		texte(300,230,"Aucune sauvegarde trouvÃ©e","white","center","Arial")
	while 1:
		x,y,_ = attente_clic()
		if y > 200:
			if exists("partie.sav"):
				return 0
		elif y > 60:
			return 2+x//200

def demande_ia(nb_joueurs):
	"""Demande le nombre d'IA et retourne le nombre sÃ©lectionnÃ©"""
	rectangle(0,0,600,60,"black","black")
	texte(300,30,"Combien d'ordinateurs ?","white","center","Arial")
	nb_joueurs += 1
	for x in range(nb_joueurs):
		rectangle((600//nb_joueurs)*x,60,(600//nb_joueurs)*x+600//nb_joueurs,200,"grey"+str(80-20*x),"grey"+str(80-20*x))
		texte((600//nb_joueurs)*x+300//nb_joueurs,130,str(x),"white","center","Arial")
	while 1:
		x,y,_ = attente_clic()
		if y > 60:
			return x//(600//nb_joueurs)

def charger_jeu(fabriques, sac, plateaux):
	"""
	Remplie les fabriques (Ã  l'exception de la fabrique 0 qui reprÃ©sente
	la zone du centre) Ã  l'aide des Ã©lÃ©ments du sac de maniÃ¨re alÃ©atoire.
	Reremplit le sac selon les rÃ¨gles s'il n'y a plus d'Ã©lÃ©ments.
        """
	for x in range(1, len(fabriques)):
		plateaux = liste_simple(plateaux)
		for y in range(4):
			fabriques[x].append(sac.pop(randint(0, len(sac)-1)))
			if len(sac) == 0:
				sac[:] = ["blue"]*20+["orange"]*20+["red"]*20+["black"]*20+["green"]*20
				for el in plateaux:
					if el in sac:
						sac.remove(el)
				if len(sac) == 0:
					break
                        
def fin_manche(plateaux, mur, score):
	"""Effectue les actions de fin de manche et renvoie le joueur qui jouera en premier au prochain tour"""
	for x in range(len(plateaux)//2):
		for y in range(len(plateaux[2*x])-1):
			if plateaux[2*x][y][-1] in ["blue","red","green","orange","black"]:
				posit = 4-mur[y].index(plateaux[2*x][y][-1])
				plateaux[2*x+1][y][posit] = plateaux[2*x][y][-1]
				plateaux[2*x][y] = ["grey"]*len(plateaux[2*x][y])
				calcul_score(plateaux, x, (y, posit), score)
		for z in range(len(plateaux[2*x][5])):
			score[x] += [-1,-1,-2,-2,-2,-3,-3][z]*(plateaux[2*x][5][z] != "grey")
			score[x] = max(score[x], 0)
		if "white" in plateaux[2*x][5]:
			prochain_joueur = x
		plateaux[2*x][5] = ["grey"]*7
	return prochain_joueur

def fin_partie(plateaux):
	"""Retourne True si la partie est terminÃ©e, False sinon"""
	for x in range(len(plateaux)//2):
		for y in range(len(plateaux[2*x+1])):
			if "grey" not in plateaux[2*x+1][y]:
				return True
	return False

def score_final(plateaux, score):
	"""Modifie les scores afin de repecter les rÃ¨gles de fin de partie"""
	for x in range(len(plateaux)//2):
		couleurs = {"green", "blue", "orange", "red", "black"}
		for y in range(len(plateaux[2*x+1])):
			if "grey" not in plateaux[2*x+1][y]:
				score[x] += 2
			if "grey" not in [plateaux[2*x+1][z][y] for z in range(5)]:
				score[x] += 7
			couleurs = couleurs.intersection(set(plateaux[2*x+1][y]))
		score[x] += len(couleurs)*10
                
def calcul_score(plateaux, x, el, score):
        """Calcule et modifie le score pour un Ã©lÃ©ment en position el"""
        mur_joueur = plateaux[2*x+1]
        n = 1
        hor_ver = [0, 0]
        for el2 in [(-1,0),(1,0),(0,1),(0,-1)]:
                m = 1
                while el[0]+el2[0]*m in range(5) and el[1]+el2[1]*m in range(5) and mur_joueur[el[0]+el2[0]*m][el[1]+el2[1]*m] is not "grey":
                        n += 1
                        m += 1
                if m != 1:
                        if el2[0] == 0:
                                hor_ver[0] = 1
                        else:
                                hor_ver[1] = 1
        score[x] += n + (hor_ver == [1, 1])

def sauvegarder_jeu(sac, plateaux, fabriques, nb_joueurs, nb_ia, score, joueur_actuel):
        """Sauvegarde la partie dans un fichier partie.sav"""
        with open("partie.sav", "w") as fic:
                fic.write("sac = " + str(sac) + "\n")
                fic.write("plateaux = " + str(plateaux) + "\n")
                fic.write("nb_joueurs = " + str(nb_joueurs) + "\n")
                fic.write("nb_ia = " + str(nb_ia) + "\n")
                fic.write("joueur_actuel = " + str(joueur_actuel) + "\n")
                fic.write("fabriques = " + str(fabriques) + "\n")
                fic.write("score = " + str(score))

def montrer_jeu(plateaux, fabriques, zone, action, joueur_actuel, score):
	"""Affiche le jeu et prÃ©pare les zones de collision."""
	zone[:] = []
	action[:] = []
	efface_tout()
	rectangle(0,0,1200,400,"grey80","grey80")

	# Affiche le jeton du premier joueur s'il n'est pas attribuÃ©
	rectangle(100*(len(plateaux)//2-1)+10,10,100*(len(plateaux)//2-1)+40,40,"white","white")
	texte(100*(len(plateaux)//2-1)+25,25,"1","black","center","Arial","12")
	for x in range(len(plateaux)//2):
		if "white" in plateaux[2*x][5]:
			rectangle(100*(len(plateaux)//2-1)+10,10,100*(len(plateaux)//2-1)+40,40,"grey80","grey80")
			break

	# Affiche les fabriques et leurs Ã©lÃ©ments
	centre = 75*len(plateaux)-25*len(fabriques)+25
	for x in range(1, len(fabriques)):
		cercle(25+50*(x-1)+centre,25,25,"white","white")
		for y in range(len(fabriques[x])):
			a,b,c,d = 13+12*(y%2)+50*(x-1)+centre, 13+12*(y//2), 25+12*(y%2)+50*(x-1)+centre, 25+12*(y//2)
			rectangle(a,b,c,d,fabriques[x][y],fabriques[x][y])
			zone.append((a,b,c,d))
			action.append(("fabriques",x,y))

	# Affiche fabriques[0], reprÃ©sentant la zone du centre
	centre = 75*len(plateaux)-10*len(fabriques[0])
	for x in range(len(fabriques[0])):
		a,b,c,d = 20*x+centre,60,20*x+20+centre,80
		rectangle(a,b,c,d,fabriques[0][x],fabriques[0][x])
		zone.append((a,b,c,d))
		action.append(("fabriques",0,x))

	# Affiche les plateaux des joueurs (Ã©lÃ©ments pairs de la variable plateaux) et les lignes dÃ©jÃ  remplis (impairs)
	for x in range(len(plateaux)):
		for y in range(len(plateaux[x])):
			if x%2 == 0 and x//2 == joueur_actuel:
				a,b,c = 140*x+120+10+40*(y==5), 110+20*y+20*(y==5), 10
				cercle(a, b, c, "red","red")
				zone.append((a-c, b-c, a+c, b+c))
				action.append(("jouer_ligne", y))
				
			for z in range(len(plateaux[x][y])):
				if y == 5:
					a,b,c,d = 140*x+20*z+20,220,140*x+20*z+40,240
					rectangle(a,b,c,d,"black",plateaux[x][y][z])
					texte(a+10,b+30,["-1","-1","-2","-2","-2","-3","-3"][z],"black","center","Arial","10")
					if plateaux[x][y][z] == "white":
						texte(a+10,b+10,"1","black","center","Arial","10")
					
				else:
					rectangle(140*x+20*(5-z),100+20*y,140*x+20*(5-z)+20,120+20*y,"black",plateaux[x][y][z])

	for x in range(len(score)):
		texte(280*x+220,230,"Score: "+str(score[x]),"black","center","Arial","12")
                        
def attendre_collision(zone, action, x, y):
	"""
	VÃ©rifie si un clic en position (x,y) touche une zone de collision, et renvoie
	l'action associÃ©e si c'est le cas, ('rien',) sinon
		
	>>> attendre_collision([(0,0,100,100)], [('action_effectuee',)], 50, 50)
	('action_effectuee',)
	>>> attendre_collision([(0,0,100,100)], [('action_effectuee',)], 150, 150)
	('rien',)
	"""
	for a in range(len(zone)):
		if zone[a][2] >= x and x >= zone[a][0] and zone[a][3] >= y and y >= zone[a][1]:
			return action[a]
	return ("rien", )

def jouer(zone, action, plateaux, joueur_actuel, sac, fabriques, nb_joueurs, nb_ia, score):
	"""Attend une action valide de la part de l'utilisateur."""	
	plateau_joueur = plateaux[2*joueur_actuel]
	suiv_action = ("rien",)
	while (suiv_action == ("rien",) or (suiv_action[1] != 5 and plateau_joueur[suiv_action[1]][0] not in ["grey",couleur])) or (suiv_action[1] != 5 and couleur in plateaux[2*joueur_actuel+1][suiv_action[1]]):
		prev_action = ("rien",)
		while prev_action[0] != "fabriques" or suiv_action[0] != "jouer_ligne":
			x,y,_ = attente_clic()
			prev_action, suiv_action = suiv_action, attendre_collision(zone,action,x,y)
			if suiv_action == ("quitter", ):
				ferme_fenetre()
				sys.exit()
			if suiv_action == ("sauvegarder", ):
				sauvegarder_jeu(sac, plateaux, fabriques, nb_joueurs, nb_ia, score, joueur_actuel)
				banniere("Partie sauvegardÃ©e !", 140*nb_joueurs, 375)
		couleur = fabriques[prev_action[1]][prev_action[2]]
	changements(plateau_joueur, joueur_actuel, prev_action, suiv_action, couleur)

def coup_ia(plateaux, joueur_actuel, fabriques):
	"""GÃ©nÃ¨re un coup alÃ©atoire pour les joueurs ordinateurs."""
	plateau_joueur = plateaux[2*joueur_actuel]
	mur_joueur = plateaux[2*joueur_actuel+1]
	n = randint(0, len(fabriques)-1)
	while len(fabriques[n]) == 0:
		n = randint(0, len(fabriques)-1)
	m = randint(0, len(fabriques[n])-1)
	prev_action = ("fabriques", n, m)
	couleur = fabriques[n][m]
	n = randint(0, 5)
	while n != 5 and (plateau_joueur[n][0] not in ["grey", couleur] or couleur in mur_joueur[n]):
		n = randint(0, 5)
	suiv_action = ("jouer_ligne", n)
	changements(plateau_joueur, joueur_actuel, prev_action, suiv_action, couleur)

def changements(plateau_joueur, joueur_actuel, prev_action, suiv_action, couleur):
	"""Effectue les changements dans le tableau du joueur"""
	n = 0
	while couleur in fabriques[prev_action[1]]:
		fabriques[prev_action[1]].remove(couleur)
		n += 1

	while "grey" in plateau_joueur[5]:
		plateau_joueur[5].pop()

	if prev_action[1] == 0:
		verif = True
		for x in range(len(plateaux)//2):
			if "white" in plateaux[2*x][5]:
				verif = False
				break
		if verif:
			plateau_joueur[5].append("white")
	else:
		fabriques[0] += fabriques[prev_action[1]]
		fabriques[prev_action[1]] = []

	if suiv_action[1] != 5:
		plateau_joueur[suiv_action[1]] = [couleur]*n + plateau_joueur[suiv_action[1]]
		plateau_joueur[5] += plateau_joueur[suiv_action[1]][suiv_action[1]+1:]
		plateau_joueur[suiv_action[1]] = plateau_joueur[suiv_action[1]][:suiv_action[1]+1]
	else:
		plateau_joueur[5] += [couleur]*n

	while len(plateau_joueur[5]) < 7:
		plateau_joueur[5].append("grey")
	plateau_joueur[5] = plateau_joueur[5][:7]

def joueur_gagnant(fabriques, score):
        """
Retourne un texte indiquant le gagnant de la partie

>>> joueur_gagnant([[],[["grey"]],[],[["red"]]], [2, 2]
"Le joueur 2 l'emporte"
>>> joueur_gagnant([[],[["blue"]],[],[["red"]]], [2, 2]
"Les joueurs 1, 2 l'emportent"
"""
        maxim = max(score)
        joueurs = []
        for x in range(len(score)):
                if score[x] == maxim:
                        joueurs.append(x)
        if len(joueurs) == 1:
                return "Le joueur " + str(joueurs[0]+1) + " l'emporte"
        joueurs2 = []
        maxim = 0
        for el in joueurs:
                n = 0
                for el2 in fabriques[el*2+1]:
                        if "grey" not in el2:
                                n += 1
                if n > maxim:
                        joueurs2 = [el+1]
                        maxim = n
                elif n == maxim:
                        joueurs2.append(el+1)
        if len(joueurs2) == 1:
                return "Le joueur " + str(joueurs2[0]) + " l'emporte"
        else:
                return "Les joueurs " + str(joueurs2)[1:-1] + " l'emportent"
                        

if __name__ == '__main__':
	cree_fenetre(600,260)
	nb_joueurs = demande_joueurs()
	if nb_joueurs == 0:
		ferme_fenetre()
		with open("partie.sav") as fic:
			text = fic.read()
			exec(text)
	else:
		ferme_fenetre()
		cree_fenetre(600,200)
		nb_ia = demande_ia(nb_joueurs)
		ferme_fenetre()
	
		fabriques = creer_matrice(2*nb_joueurs+2)
		plateaux = creer_matrice(2*nb_joueurs)
		for x in range(nb_joueurs):
			plateaux[2*x] = creer_matrice(6,1,6/5)
			plateaux[2*x+1] = creer_matrice(5,5)

		sac = ["blue"]*20+["orange"]*20+["red"]*20+["black"]*20+["green"]*20
		charger_jeu(fabriques, sac, plateaux)
		score = [0]*nb_joueurs
		joueur_actuel = 0

	with open("mur.config") as fic:
		exec(fic.read())
	zone_collisions = []
	action_collisions = []
	cree_fenetre(280*nb_joueurs,400)

	while not fin_partie(plateaux):
		while not matrice_videe(fabriques):
			montrer_jeu(plateaux, fabriques, zone_collisions, action_collisions, joueur_actuel, score)
			banniere("Tour du joueur "+str(joueur_actuel+1), 140*nb_joueurs, 375)
			if joueur_actuel < nb_joueurs-nb_ia:
				bouton("Quitter", 70*len(plateaux)-70, 300, zone_collisions, action_collisions, ("quitter",))
				bouton("Sauv.", 70*len(plateaux)+70, 300, zone_collisions, action_collisions, ("sauvegarder",))
				jouer(zone_collisions, action_collisions, plateaux, joueur_actuel, sac, fabriques, nb_joueurs, nb_ia, score)
			else:
				attente_touche_jusqua(100)
				coup_ia(plateaux, joueur_actuel, fabriques)
			joueur_actuel = (joueur_actuel+1) % nb_joueurs

		joueur_actuel = fin_manche(plateaux, mur, score)
		montrer_jeu(plateaux, fabriques, zone_collisions, action_collisions, 4, score)
		banniere("Manche terminÃ©e", 140*nb_joueurs, 375)
		attente_clic()
		charger_jeu(fabriques, sac, plateaux)

	score_final(plateaux, score)
	montrer_jeu(plateaux, fabriques, zone_collisions, action_collisions, 4, score)
	banniere("La partie est terminÃ©e", 140*nb_joueurs, 375)
	attente_touche_jusqua(3000)
	banniere(joueur_gagnant(fabriques, score), 140*nb_joueurs, 375)
	attente_clic()
	ferme_fenetre()
    