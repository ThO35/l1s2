from fltk import*
from math import*
from collections import deque
from queue import*
from pygame.locals import *
from pygame import mixer


#partie pour initialiser la musique
mixer.init()
mixer.music.load('sultan.wav')
mixer.music.play()

lignes = 500
colonne = 500
police = "Arial Black"
taille = 50



cree_fenetre(lignes,colonne)


def jeux1 (ligne,colonne,fichier):
    mort = []
    tresor = ""
    patern = { "═":(False,True,False,True),

            "║":(True,False,True,False),

            "╔":(False,True,True,False),

            "╗":(False,False,True,True),

            "╚":(True,True,False,False),

            "╝":(True,False,False,True),

            "╠":(True,True,True,False),

            "╣":(True,False,True,True),

            "╦":(False,True,True,True),

            "╩":(True,True,False,True),

            "╨":(True,False,False,False),

            "╡":(False,False,False,True),

            "╥":(False,False,True,False),

            "╞":(False,True,False,False),

            "╬":(True,True,True,True),}



    ## charger
    def charge(fichier):
        """
        Charge les données du fichier spécifié dans un dictionnaire.

        Args:
            fichier (str): Le chemin vers le fichier contenant les données à charger.

        Returns:
            dict: Un dictionnaire contenant les données du fichier chargé.

        """       
        resultats = {}
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                lignes = f.readlines()
                for i, ligne in enumerate(lignes):
                    donnees = ligne.encode('utf-8')
                    donnees_decodees = donnees.decode('utf-8', errors='replace')
                    if donnees_decodees[0] == "A":
                        resultats["a"] = donnees_decodees.strip()
                    elif donnees_decodees[0] == "D":
                        resultats["d"+str(donnees_decodees[6])] = donnees_decodees.strip()
                    else :
                        resultats["l"+str(i+1)] = donnees_decodees.strip()
        except Exception as e:
            print("Erreur lors du décodage des données :", str(e))
        return resultats


    ## formation_donjon
    def formation_donjon (donnees_fichier,patern):
        """
        Crée des donjons à partir des données du fichier et du modèle de construction spécifié.

        Args:
            donnees_fichier (dict): Dictionnaire des données du fichier à utiliser pour créer les donjons.
            patern (dict): Dictionnaire représentant le modèle de construction des donjons.

        Returns:
            list: Liste des donjons créés.
        """       
        donjons_forme = []
        for valeur ,cle in donnees_fichier.items():
            if cle [0] == "A":
                break
            else :
                lignes_donjon=[]
                for i in range (0,len(cle)) :
                    for valeur1,cle1 in patern.items():
                        if cle[i] == valeur1:
                            dic= []
                            for m in cle1:
                                dic.append(m)
                            lignes_donjon.append (dic)
                donjons_forme.append(lignes_donjon)
        return donjons_forme

    ## Information Dragon est Hero
    def  hero (donnees_fichier):
        """
        Extrait les informations du héros à partir des données du fichier.

        Args:
            donnees_fichier (dict): Dictionnaire des données du fichier à utiliser pour extraire les informations
                                    du héros.

        Returns:
            dict: Dictionnaire contenant la position et le niveau du héros.

        """
        hero = {}
        for valeur ,cle in donnees_fichier.items():
            if cle [0] == "A":
                hero["position"] = (int(cle[2]),int(cle[4]))
                if len(cle)<6:
                    hero ["niveau"] = 1
                else:
                    hero ["niveau"]=int (cle[6])
        return hero
    
    def dragons (donnees_fichier):
        """
        Extrait les informations sur les dragons à partir des données du fichier.

        Args:
            donnees_fichier (dict): Dictionnaire contenant les données du fichier à partir desquelles les
                                    informations sur les dragons doivent être extraites.

        Returns:
            list: Une liste de dictionnaires contenant les informations sur chaque dragon présent dans le donjon.

        """ 
        dragons = []
        for valeur ,cle in donnees_fichier.items():
            dragonsdico = {}
            if cle [0] == "D":
                dragonsdico["position"] = (int(cle[2]),int(cle[4]))
                dragonsdico["niveau"] = int(cle[6])
                dragons.append (dragonsdico)
        return dragons

    ## Pivot
    def pivoter (position,donnees_fichier,patern ):
        """
        Pivoter le symbole à la position spécifiée en fonction du modèle de rotation fourni.

        Args:
            position (tuple): Le tuple représentant la position (ligne, colonne) du symbole à pivoter.
            donnees_fichier (dict): Le dictionnaire contenant les données du fichier.
            patern (dict): Le dictionnaire contenant les modèles de rotation des symboles.

        Returns:
            None
        """
        n=0
        for cle, valeur in donnees_fichier.items():
            chaine = valeur
            if cle  == "a":
                break
            else:
                m=0
                for valeur in valeur:
                    if n == position[0] and m == position [1]:
                        nouveau_caractere = symbolepivot (patern,valeur)
                        donnees_fichier[cle] = souspivot (chaine,position[1],nouveau_caractere)
                    m+=1
            n+=1
    def symbolepivot (patern,symbole):
        """
        Rotation du symbole selon le modèle de rotation fourni.

        Args:
            patern (dict): Le dictionnaire contenant les modèles de rotation des symboles.
            symbole (str): Le symbole à faire pivoter.

        Returns:
            str: Le symbole pivoté.

        """
        for valeur, cle in patern.items():
            if valeur  == symbole:
                retour = list (cle)
                retour.insert (0,retour.pop())
                for valeur, cle in patern.items():
                    if list (cle) == retour:
                        return valeur
    def souspivot (chaine,position,nouveau_caractere):
        """
        Remplacer le caractère à la position spécifiée par le nouveau caractère.

        Args:
            chaine (str): La chaîne de caractères dans laquelle effectuer la rotation.
            position (int): La position à laquelle effectuer la rotation.
            nouveau_caractere (str): Le nouveau caractère à insérer.

        Returns:
            str: La chaîne de caractères avec le nouveau caractère inséré à la position spécifiée.
        """
        chaine = list(chaine)
        chaine[position] = nouveau_caractere
        return ''.join(chaine)

    ## Rencontre
    def rencontre(mort):
        """
        Vérifie si l'aventurier rencontre un dragon sur sa case actuelle et gère la logique de jeu correspondante.
        Si l'aventurier rencontre un dragon, la fonction renvoie False et supprime l'aventurier du fichier de données.
        Si l'aventurier rencontre un dragon de niveau égal, le dragon est supprimé du fichier de données et l'aventurier passe au niveau supérieur.
        Si l'aventurier rencontre un dragon de niveau supérieur, la fonction renvoie False et supprime l'aventurier du fichier de données.
        Si tous les dragons ont été vaincus, la fonction renvoie True.

        Args:
        - mort (list): une liste qui contient les dragons vaincus.

        Returns:
        - (bool) True si tous les dragons ont été vaincus, False sinon.
        """
        dragon = dragons(donnees_fichier)
        aventurier = hero(donnees_fichier)
        for i in dragon:
            if i["position"] == aventurier["position"]:
                if i["niveau"] != aventurier["niveau"]:
                    del donnees_fichier["a"]
                    return False
                else:
                    if len (dragon )== 3:
                        mort.append(donnees_fichier["d1"])
                        del donnees_fichier["d1"]
                        m=donnees_fichier["a"]
                        donnees_fichier["a"] = m[0]+m[1]+m[2]+m[3]+m[4]+m[5]+"2"
                    if len (dragon )== 2:
                        mort.append(donnees_fichier["d2"])
                        del donnees_fichier["d2"]
                        m=donnees_fichier["a"]
                        donnees_fichier["a"] = m[0]+m[1]+m[2]+m[3]+m[4]+m[5]+"3"
                    if len (dragon )== 1:
                        mort.append(donnees_fichier["d3"])
                        del donnees_fichier["d3"]
                        return False
                    return True

    def appliquer_chemin(chemin,tresor):
        """
        Cette fonction prend un chemin (une liste de coordonnées) en entrée et met à jour les données du jeu pour déplacer le héros le long de ce chemin.
        Si le héros rencontre un dragon en cours de route, la fonction appelle la fonction rencontre() pour résoudre l'affrontement.
        Si le héros réussit à atteindre la fin du chemin sans être tué, la fonction renvoie True.
        Si le héros meurt en cours de route, la fonction renvoie False.
        """
        # Déplacer l'aventurier le long du chemin
        for position in chemin:
            m = donnees_fichier["a"]
            if len(m)<6:
                donnees_fichier["a"]= "A " +str(position[0])+ " "+str(position[1])+" "+str(1)
            else:
                donnees_fichier["a"]= "A " +str(position[0])+ " "+str(position[1])+" "+str(m[6])
            coor = table3 (lignes,colonne,donjons,donnees_fichier,tresor)
            chemins (ligne,colonne,tresor)
            m= rencontre(mort)
            if m == False:
                return False
            mise_a_jour()

    def fin_partie ():
        if len(dragons(donnees_fichier)) == 0:
            return 1
        if hero(donnees_fichier) == {} :
            return -1
        return 0

    ## Trouver le Chemin

    def intention(donjon, position, dragons, tresor):
        """
        Recherche le chemin le plus court pour atteindre le trésor tout en évitant les dragons.

        Args:
        - donjon (list[list[int]]): une matrice représentant le donjon, où chaque case est soit un mur (représenté par 1),
        soit un couloir (représenté par 0).
        - position (tuple[int, int]): la position de départ du personnage dans le donjon.
        - dragons (list[dict]): une liste de dictionnaires représentant les dragons, où chaque dictionnaire a les clés
        "position" (une tuple représentant la position du dragon dans le donjon) et "niveau" (un entier représentant le
        niveau de difficulté du dragon).
        - tresor (tuple[int, int]): la position du trésor dans le donjon.

        Returns:
        - list[tuple[int, int]]: le chemin optimal pour atteindre le trésor tout en évitant les dragons, représenté par une
        liste de tuples représentant les positions dans le donjon. Si le trésor est inaccessible, retourne None.
        """
        max_niveau = 0
        chemin_optimal = None
        file = deque([(position, [])])
        visite = set()
        tresors_disponibles = [tresor]

        while file:
            position_courante, chemin_courant = file.popleft()

            if position_courante in visite:
                continue

            visite.add(position_courante)

            for dragon in dragons:
                if position_courante == dragon["position"] and dragon["niveau"] > max_niveau:
                    max_niveau = dragon["niveau"]
                    chemin_optimal = chemin_courant + [position_courante]

            for voisin in [(position_courante[0]-1, position_courante[1]), (position_courante[0]+1, position_courante[1]),
                        (position_courante[0], position_courante[1]-1), (position_courante[0], position_courante[1]+1)]:

                if voisin[0] < 0 or voisin[0] >= len(donjon) or voisin[1] < 0 or voisin[1] >= len(donjon[0]):
                    continue

                if not connecte(donjon, position_courante, voisin, max_niveau, dragons):
                    continue

                if voisin in visite:
                    continue

                if voisin in tresors_disponibles:
                    tresors_disponibles.remove(voisin)
                    chemin_optimal = chemin_courant + [position_courante, voisin]
                    return chemin_optimal

                file.append((voisin, chemin_courant + [position_courante]))

            if position_courante == tresor:
                tresors_disponibles.remove(tresor)

        return chemin_optimal


    def connecte(donjon, position1, position2, max_niveau, dragons):
        """
        Vérifie si deux positions sont adjacentes et reliées par une porte dans un donjon,
        tout en prenant en compte la présence des dragons.

        Args:
        - donjon (list[list[list[int]]]): une matrice représentant le donjon, où chaque case est une liste de 4 valeurs
        booléennes représentant les murs et les portes dans les directions N, E, S, W.
        - position1 (tuple[int, int]): les coordonnées de la première position.
        - position2 (tuple[int, int]): les coordonnées de la deuxième position.
        - max_niveau (int): le niveau de difficulté maximal parmi les dragons présents.
        - dragons (list[dict]): une liste de dictionnaires représentant les dragons, où chaque dictionnaire a les clés
        "position" (une tuple représentant la position du dragon dans le donjon) et "niveau" (un entier représentant le
        niveau de difficulté du dragon).

        Returns:
        - bool: True si les deux positions sont adjacentes et reliées par une porte et aucun dragon de niveau supérieur n'est
        présent sur les positions, False sinon.

        """
        if not (0 <= position1[0] < len(donjon) and 0 <= position1[1] < len(donjon[0])
                and 0 <= position2[0] < len(donjon) and 0 <= position2[1] < len(donjon[0])):
            print(f"Positions non valides : {position1}, {position2}")
            return False

        if position2[0] == position1[0]+1:
            for dragon in dragons:
                if dragon["niveau"] <= max_niveau and dragon["position"] in [position1, position2]:
                    return False
                if not donjon[position1[0]][position1[1]][2] or not donjon[position2[0]][position2[1]][0]:
                    return False
            else:
                return True

        if position2[0] == position1[0]-1:
            for dragon in dragons:
                if dragon["niveau"] <= max_niveau and dragon["position"] in [position1, position2]:
                    return False
                if not donjon[position1[0]][position1[1]][0] or not donjon[position2[0]][position2[1]][2]:
                    return False
            else:
                return True

        if position2[1] == position1[1]-1:
            for dragon in dragons:
                if dragon["niveau"] <= max_niveau and dragon["position"] in [position1, position2]:
                    return False
                if not donjon[position1[0]][position1[1]][3] or not donjon[position2[0]][position2[1]][1]:
                    return False
            else:
                return True

        if position2[1] == position1[1]+1:
            for dragon in dragons:
                if dragon["niveau"] <= max_niveau and dragon["position"] in [position1, position2]:
                    return False
                if not donjon[position1[0]][position1[1]][1] or not donjon[position2[0]][position2[1]][3]:
                    return False

            else:
                return True

        if abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]) != 1:
            print(f"Positions non adjacentes : {position1}, {position2}")

        return False

    ## Dessin

    def table3 (lignes,colonne,donjons,donnees_fichier,tresor):
        """
        Génère une table de coordonnées pour les donjons et les trésors.

        Args:
            lignes (int): Le nombre de lignes de la table.
            colonne (int): Le nombre de colonnes de la table.
            donjons (list): Une liste contenant les données des donjons.
            donnees_fichier (str): Le nom du fichier contenant les données.
            tresor (str): Le nom du trésor.

        Returns:
            list: Une liste de coordonnées représentant la table de donjons.

        """
        efface_tout()
        maxx = 0
        for i in donjons:
            if maxx <= len(i):
                maxx= len(i)
        maxy = len (donjons)
        coor = []
        for x in range (0,maxx):
            lignecoor = []
            for y in range (0,maxy):
                x1 = (lignes/maxx)*x
                y1 = (colonne/maxy)*y
                x2 = (lignes/maxx)*(x+1)
                y2 = (colonne/maxy)*(y+1)
                lignecoor.append([x1,y1,x2,y2])
                posemap (x1,x2,y1,y2,donnees_fichier,x,y)
                pose (x1,x2,y1,y2,donnees_fichier,x,y,mort,tresor)
            coor.append (lignecoor)
        return coor


    def table2 (lignes,colonne,donjons,donnees_fichier,patern,clic,tresor):
        """
        Génère une table de coordonnées pour les donjons et les trésors, et effectue une action de pivotement.

        Args:
            lignes (int): Le nombre de lignes de la table.
            colonne (int): Le nombre de colonnes de la table.
            donjons (list): Une liste contenant les données des donjons.
            donnees_fichier (str): Le nom du fichier contenant les données.
            patern (str): Le motif de pivotement.
            clic (tuple): Les coordonnées de clic.
            tresor (str): Le nom du trésor.

        Returns:
            list: Une liste de coordonnées représentant la table de donjons.

        """
        efface_tout()
        n=0
        maxx = 0
        for i in donjons:
            if maxx <= len(i):
                maxx= len(i)
        maxy = len (donjons)
        coor = []
        for x in range (0,maxx):
            lignecoor = []
            for y in range (0,maxy):
                x1 = (lignes/maxx)*x
                y1 = (colonne/maxy)*y
                x2 = (lignes/maxx)*(x+1)
                y2 = (colonne/maxy)*(y+1)
                lignecoor.append([x1,y1,x2,y2])
                posemap (x1,x2,y1,y2,donnees_fichier,x,y)
                pose (x1,x2,y1,y2,donnees_fichier,x,y,mort,tresor)

            coor.append (lignecoor)
        p=(positionxy(coor,clic))
        pivoter (p,donnees_fichier,patern )
        n+=1
        table3 (lignes,colonne,donjons,donnees_fichier,tresor)
        return coor


    def table (tresor):
        """
        Fonction principale qui lance le jeu et gère les actions du joueur.

        Args:
            tresor (str): Le nom du trésor initial.

        Returns:
            str: L'état de la partie (finie ou non).

        """
        table3 (lignes,colonne,donjons,donnees_fichier,tresor)
        nbr_diament = 2
        verifi = True
        while verifi == True or verifi == None:
            ev = donne_ev()
            tev = type_ev(ev)
    # Si une touche est apuyer devra lancais le fonction intention dessiner le chemin et deplacer le chevalier. Bien sur verifier l'etat du jeux. Si c'est la fin doit return Fales sinon True
            table3 (lignes,colonne,donjons,donnees_fichier,tresor)
            chemins (ligne,colonne,tresor)
            if tev == 'Touche':
                if touche(ev) == "space":
                    donjon=formation_donjon (donnees_fichier,patern)
                    position= hero(donnees_fichier)['position']
                    dragon = dragons(donnees_fichier)
                    chemin = intention(donjon, position,dragon,tresor)
                    if chemin != None:
                        intention(donjon, position,dragon,tresor)
                        verifi = appliquer_chemin(chemin,tresor)
                        if hero(donnees_fichier) != {}:
                            if hero(donnees_fichier)['position'] == tresor:
                                tresor = "fin"
                                mise_a_jour()
                elif touche(ev) == 'r':
                    #permet au joueur de reprendre la partie
                    jeux1(lignes,colonne,fichier)
                elif touche(ev) == 'Escape':
                    #permet au joueur de revenir au menu pour choisir un autre jeu
                    page2()
    # Permet de faire des rotations.
            elif tev == "ClicGauche":
                clic = (abscisse(ev),ordonnee(ev))
                table2 (lignes,colonne,donjons,donnees_fichier,patern,clic,tresor)

            elif tev == "ClicDroit":
                if nbr_diament != 0:
                    clic = (abscisse(ev),ordonnee(ev))
                    coor =table3 (lignes,colonne,donjons,donnees_fichier,tresor)
                    (positionxy(coor,clic))
                    tresor = (positionxy(coor,clic))
                    nbr_diament -= 1
            elif tev == 'Quitte':
                break 
            mise_a_jour()

        return fin_partie ()


    def posemap (x1,x2,y1,y2,donnees_fichier,x,y):
        """
        Affiche l'image correspondante à la position (x, y) sur la carte de jeu.

        Args:
            x1 (float): La position x du coin supérieur gauche de la carte.
            x2 (float): La position x du coin inférieur droit de la carte.
            y1 (float): La position y du coin supérieur gauche de la carte.
            y2 (float): La position y du coin inférieur droit de la carte.
            donnees_fichier (dict): Un dictionnaire contenant les données des différents éléments de la carte.
            x (int): La coordonnée x de la position à afficher.
            y (int): La coordonnée y de la position à afficher.

        Returns:
            None
        """
        n = 0
        for valeur,cle in donnees_fichier.items():
            m=0
            for valeur in cle:
                if n == y and m==x:
                    image ((x1+x2)/2,(y1+y2)/2,str(valeur)+".png",largeur=int ((x2-x1)), hauteur=int(y2-y1) , ancrage='center',tag='cle')
                m+=1
            n+=1


    def pose (x1,x2,y1,y2,donnees_fichier,x,y,mort,tresor):
        """
        Pose les éléments du jeu aux coordonnées spécifiées sur la table.

        Args:
            x1 (float): Coordonnée x du coin supérieur gauche de la case.
            x2 (float): Coordonnée x du coin inférieur droit de la case.
            y1 (float): Coordonnée y du coin supérieur gauche de la case.
            y2 (float): Coordonnée y du coin inférieur droit de la case.
            donnees_fichier (dict): Les données du fichier de jeu.
            x (int): Coordonnée x de la case dans la table.
            y (int): Coordonnée y de la case dans la table.
            mort (list): Liste des éléments morts dans le jeu.
            tresor (str or tuple): Le nom du trésor ou un tuple contenant les coordonnées du trésor.

        """       
        for valeur,cle in donnees_fichier.items():
            if valeur == "a" and (cle[4] == str(x) and cle[2] == str(y)) :
                image ((x1+x2)/2,(y1+y2)/2,"niv"+str(niv(niveau))+".png",largeur=50, hauteur=50, ancrage='center')
            if valeur == "d1" and (cle[4] == str(x) and cle[2] == str(y)) :
                image ((x1+x2)/2,(y1+y2)/2,"dragon1 "+str(niv(niveau))+".png",largeur=50, hauteur=50, ancrage='center')
            if valeur == "d2" and (cle[4] == str(x) and cle[2] == str(y)) :
                image ((x1+x2)/2,(y1+y2)/2,"dragon2 "+str(niv(niveau))+".png",largeur=50, hauteur=50, ancrage='center')
            if valeur == "d3" and (cle[4] == str(x) and cle[2] == str(y)):
                image ((x1+x2)/2,(y1+y2)/2,"dragon3 "+str(niv(niveau))+".png",largeur=50, hauteur=50, ancrage='center')
        for i in mort:
            if i[4] == str (x) and i[2]==str (y):
                image ((x1+x2)/2,(y1+y2)/2,"mort.png",largeur=50, hauteur=50,
    ancrage='center',tag='mort')

        if isinstance(tresor, tuple):
            if x == tresor[1] and y == tresor[0]:
                image ((x1+x2)/2,(y1+y2)/2,"treasure.png",largeur=50, hauteur=50,
    ancrage='center',tag='mort')
            chemins (ligne,colonne,tresor)


    def positionxy (coor,clic):
        """
        Renvoie les coordonnées de la case correspondante aux coordonnées du clic.

        Args:
            coor (list): Liste des coordonnées des cases de la table.
            clic (tuple): Coordonnées du clic.

        Returns:
            tuple: Coordonnées de la case correspondante.

        """
        x= clic[0]
        y= clic[1]
        positionx = 0
        for i in coor:
            positiony=0
            for j in i:
                if j[0]<= x <= j[2]:
                    if j[1]<= y <= j[3]:
                        return (positiony,positionx)
                positiony+=1
            positionx+=1


    def chemins (ligne,colonne,tresor):
        """
        Trace les chemins entre les cases du donjon.

        Args:
            ligne (function): Fonction pour tracer une ligne.
            colonne (function): Fonction pour tracer une colonne.
            tresor (str or tuple): Le nom du trésor ou un tuple contenant les coordonnées du trésor.

        """
        maxx = 0
        for i in donjons:
            if maxx <= len(i):
                maxx= len(i)
        maxy = len (donjons)
        coor = []
        for x in range (0,maxx):
            lignecoor = []
            for y in range (0,maxy):
                x1 = (lignes/maxx)*x
                y1 = (colonne/maxy)*y
                x2 = (lignes/maxx)*(x+1)
                y2 = (colonne/maxy)*(y+1)
                lignecoor.append([x1,y1,x2,y2])
            coor.append (lignecoor)
        donjon=formation_donjon (donnees_fichier,patern)
        position= hero(donnees_fichier)['position']
        dragon = dragons(donnees_fichier)
        chemin= intention(donjon, position,dragon,tresor)
        if chemin!=None:
            p=0
            while p!= len (chemin)-1:
                first=""
                seconde=""
                n=0
                for i in coor:
                    m=0
                    for j in i:
                        if n== chemin[p][0] and m == chemin[p][1]:
                            first = j
                        m+=1
                    n+=1
                n=0
                for i in coor:
                    m=0
                    for j in i:
                        if n== chemin[p+1][0] and m == chemin[p+1][1]:
                            seconde = j
                        m+=1
                    n+=1
                p+=1

                ligne ((first[1]+first[3])/2,(first[0]+first[2])/2,(seconde[1]+seconde[3])/2,(seconde[0]+seconde[2])/2,"red",4)
    ## Jeux
    def niv (niveau):
        """
        Retourne la valeur du niveau.

        Args:
            niveau (int): Le niveau.

        Returns:
            int: La valeur du niveau.

        """
        return niveau



    def correcte(donnees_fichier):
        """
        Vérifie si les données du fichier sont correctement formatées.

        Args:
            donnees_fichier (dict): Les données extraites du fichier.

        Returns:
            int: 1 si les données sont correctes, -1 sinon.

        """
        n = 0
        premier = 0
        for valeur, cle in donnees_fichier.items():
            if valeur[0] == "l":
                second = len(cle)
                if n == 0 or premier == second:
                    premier = second
                    n += 1
                else:
                    if premier != second:
                        return -1
        if n == premier:
            return 1
        else:
            return -1
        
    niveau =0
    while niveau < len (fichier):
        mort.clear()
        donnees_fichier = charge(fichier[niveau])
        donjons = formation_donjon (donnees_fichier,patern)
        verifi = correcte (donnees_fichier)
        if verifi != -1:
            fin = table (tresor)
            if fin == -1:
                efface_tout()
                image (lignes/2,colonne/2,"rip.png")
                attend_ev()
                efface_tout ()
                mort.clear()
                efface('mort')


            if fin == 1:
                niveau+= 2
                efface_tout ()
                mort.clear()
                efface('mort')
        else:
            print ("Donjons non adaptés. On lance les suivants.")
            niveau+=1
    image (lignes/2,colonne/2,"the_end.png ",hauteur=colonne, largeur=lignes, ancrage='center')



"""
    Menu du jeu
"""
def clic():
    """
        s'occupe de gerer la souris
    """
    return attend_clic_gauche()

def page1():
    """
        fonction pour la page d'accueil
    """
    image(120, 120, 'back.png',tag='im')
    chaine = "Wall Is You !"
    texte(lignes//2, colonne//6, chaine,
        police=police, taille=taille, couleur="white",
        ancrage='center')

    texte (lignes/2, colonne/2, "Play" ,police=police, taille=taille, couleur="green",
        ancrage='center')
    x,y = clic()  
    if x:
        page2()

def Rules():
    chaine = """
   * Pour jouer 
Clic gauche: pour pivoter les cases
Clic droit: pour poser un diament(1 ou 2)
Echap: pour revenir au menu
r: pour recommencer la partie

* Clic pour revenir au menu
"""
    image(120, 120, 'back.png',tag='im')
    texte(lignes/2, colonne/2, chaine,
        police=police, taille=15, couleur="white",
        ancrage='center')
    if clic():
        page2()

def page2():
    """
        page pour donner un choix au joueur, soit jouer une partie random ou choisir le donjon, ou continuer une ancienne partie, 
        ou regarder les regle du jeu
    """
    image(120, 120, 'back.png',tag='im')
    texte(lignes/2, (colonne/8)*2, "Play",
        police=police, taille=taille, couleur="white",
        ancrage='center')
    
    texte(lignes/2, (colonne/8)*4, "Mode de Jeu",
        police=police, taille=taille, couleur="white",
        ancrage='center')

    texte(lignes/2, (colonne/8)*6, "Rules",
        police=police, taille=taille, couleur="white",
        ancrage='center')
    
    x,y = clic()
    if lignes/10<= x <=(lignes/3)*2 and colonne/5 <= y <=colonne/3:
        fichier = ["map_test.txt","map1.txt","map2.txt","map3.txt","map4.txt"]
        jeux1(ligne,colonne,fichier)       
    elif lignes/6<= x <=(lignes/3)*2 and colonne/3<= y <= (colonne/3)*2:
        mode_de_jeu()
    elif lignes/3<= x <= (lignes/3)*2 and (colonne/3)*2<= y:
        Rules()


def mode_de_jeu():
    
    image(120, 120, 'back.png',tag='im')
    texte(lignes/2, (colonne/8)*2,"Donjon 1",
        police=police, taille=taille, couleur="white",
        ancrage='center')

    texte(lignes/2, (colonne/8)*4, "Donjon 2",
        police=police, taille=taille, couleur="white",
        ancrage='center')

    texte(lignes/2, (colonne/8)*6, "Donjon 3",
        police=police, taille=taille, couleur="white",
        ancrage='center')
    choix_donjon()

def choix_donjon():
    x,y = attend_clic_gauche()
    if lignes/10<= x <=(lignes/3)*2 and colonne/5 <= y <=colonne/3:
        fichier = ["map2.txt"]
        jeux1(ligne,colonne,fichier)
    elif lignes/6<= x <=(lignes/3)*2 and colonne/3<= y <= (colonne/3)*2:
        fichier = ["map3.txt"]
        jeux1(ligne,colonne,fichier)
    elif lignes/3<= x <= (lignes/3)*2 and (colonne/3)*2<= y:
        fichier = ["map4.txt"]
        jeux1(ligne,colonne,fichier)

page1()


attend_ev()
ferme_fenetre()
