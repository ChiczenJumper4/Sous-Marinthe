import random
import copy

# Fonctions
def map_generation(taille : tuple, player_pos_start : tuple):
    """
    Génère la carte du jeu sous la forme d'une liste de listes composées de
    '*' pour les collectibles, de 'O' pour le joueur et de ' ' pour une case vide.
    Ainsi que les barrières invisibles par colonne et par ligne
    """

    assert type(taille) == tuple, "la taille doit être un tuple"
    assert type(player_pos_start) == list, "la position de départ du joueur doit être une liste"
    # création de la carte
    map = []
    for i in range(taille[1]):
        map.append([])
        for k in range(taille[0]):
            map[i].append('*')

    # position du joueur
    map[player_pos_start[0]][player_pos_start[1]] = 'O'

    # barrières (à modifier pour que cela soit tout le temps possible plus tard)
    barrieres = ([], [])
    for i in range(2):
        for k in range(taille[0]):
            barrieres[i].append([])
            for j in range(taille[1]-1):
                barrieres[i][k].append(random.randint(0,1))

    # Création d'un chemin possible
    barrieres = creation_chemin(barrieres, taille)

    # retourne la map et les barrières
    return map, barrieres

def creation_chemin(barrieres: tuple, taille_carte: list)->tuple:
    '''
    Création d'un chemin que le joueur pourras emprunter pour rendre possible toutes les cartes générées aléatoirements
    '''
    nb_case = taille_carte[0]*taille_carte[1]
    nb_case_chemin = 0
    cases_visitees = set()
    pos = [0,0]
    cases_visitees.add(tuple(pos))

    while nb_case_chemin < nb_case:
        deplacement = []
        direction_mouvement = random.randint(0,3)

        if (direction_mouvement == 0) and (pos[0]>0):
            deplacement.append((-1,0))
            direction = 0
        elif (direction_mouvement == 1) and (pos[0]<taille_carte[0]-1):
            deplacement.append((1,0))
            direction = 0
        elif (direction_mouvement == 2) and (pos[1]>0):
            deplacement.append((0,-1))
            direction = 1
        elif (direction_mouvement == 3) and (pos[1]<taille_carte[1]-1):
            deplacement.append((0,1))
            direction = 1

        if deplacement:
            dx, dy = random.choice(deplacement)
            pos[0]+=dx
            pos[1]+=dy
            if not(tuple(pos) in deplacement):
                cases_visitees.add(tuple(pos))
                nb_case_chemin+=1

            if direction == 0:
                barrieres[0][pos[1]][pos[0]-1] = 0
            elif direction == 1:
                barrieres[1][pos[0]][pos[1]-1] = 0

    return barrieres


def move(player_input : str, grille_sauvegarde : list, player_pos : list, new_map : list) -> list:
    """
    Permet le déplacement du joueur dans la carte à l'aide du mot de déplacement que l'on souhaite réaliser
    """
    assert type(grille_sauvegarde) == tuple, "la carte (grille_sauvegarde) n'est pas du bon type (doit être un tuple)"
    assert type(new_map) == tuple, "la carte (new_map) n'est pas du bon type (doit être un tuple)"
    assert type(player_pos) == list, "la position du joueur n'est pas du bon type (doit être une liste)"
    assert type(player_input) == str, "le player_input n'est pas du bon type (doit être une chaîne de caractères)"
    # Vérification du déplacement
    if player_input == 'haut':
        if player_pos[1] == 0:
            print('Vous ne pouvez pas aller plus haut.')
        elif new_map[1][1][player_pos[0]][player_pos[1]-1] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[1] -= 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'bas':
        if player_pos[1] == taille_carte[1]-1:
            print('Vous ne pouvez pas aller plus bas.')
        elif new_map[1][1][player_pos[0]][player_pos[1]] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[1] += 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'gauche':
        if player_pos[0] == 0:
            print('Vous ne pouvez pas aller plus à gauche.')
        elif new_map[1][0][player_pos[1]][player_pos[0]-1] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[0] -= 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'droite':
        if player_pos[0] == taille_carte[0]-1:
            print('Vous ne pouvez pas aller plus à droite.')
        elif new_map[1][0][player_pos[1]][player_pos[0]] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[0] += 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    return new_map, player_pos

def jeux(taille_carte : list, fenetre):
    print('')
    player_pos = [0, 0]
    case_sans_étoile = 0
    player_input = ""

    # Génération de la map et premier affichage de la grille
    grille = map_generation(taille_carte, player_pos)
    grille_sauvegarde = copy.deepcopy(grille)

    # Affichage de la carte
    mouvement = move(player_input, grille_sauvegarde, player_pos, grille)
    player_pos = copy.deepcopy(mouvement[1])
    grille = copy.deepcopy(mouvement[0])

    # Affichage de la carte
    afficher_carte(taille_carte, grille[0], fenetre)

    for i in range(len(grille[0])):
        for k in grille[0][i]:
            if k != '*':
                case_sans_étoile += 1
            if case_sans_étoile == taille_carte[0]*taille_carte[1]:
                print('Vous avez gagné!!!')
                running = False

        case_sans_étoile = 0