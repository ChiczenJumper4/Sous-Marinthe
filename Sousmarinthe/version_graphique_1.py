import pygame
from pygame.locals import *
import random
import copy

# Faire des 'cd' si chemin d'accès pas bon


# Fonctions
def map_generation(taille : list, player_pos_start : tuple)->tuple:
    """
    Génère la carte du jeu sous la forme d'une liste de listes composées de
    '*' pour les collectibles, de 'O' pour le joueur et de ' ' pour une case vide.
    Ainsi que les barrières invisibles par colonne et par ligne
    """

    assert type(taille) == list, "la taille doit être une liste"
    assert type(player_pos_start) == list, "la position de départ du joueur doit être une liste"
    
    # création de la carte
    map = []
    for i in range(taille[1]):
        map.append([])
        for k in range(taille[0]):
            map[i].append('*')

    # position du joueur
    map[player_pos_start[0]][player_pos_start[1]] = 'O'

    # Création des batrrières
    barrieres = ([], [])
    for i in range(2):
        for k in range(taille[0]):
            barrieres[i].append([])
            for j in range(taille[1]-1):
                barrieres[i][k].append(1)

    # Création d'un chemin possible
    barrieres = creation_chemin(barrieres, taille)

    # retourne la map et les barrières
    return map, barrieres

def creation_chemin(barrieres: tuple, taille_carte: list)->tuple:
    '''
    Création d'un chemin que le joueur pourras emprunter pour rendre possible toutes les cartes générées aléatoirements
    '''
    assert type(barrieres) == tuple, 'barrieres devrait etre un tuple'
    assert type(taille_carte) == list, 'taille_carte devrait etre une liste'


    nb_case = taille_carte[0]*taille_carte[1]
    nb_case_chemin = 0
    cases_visitees = set()
    pos = [0,0]
    cases_visitees.add(tuple(pos))

    # Boucle qui tourne tant que toutes les cases n'ont pas été visitées
    while len(cases_visitees) < nb_case:
        deplacement = []
        direction_mouvement = random.randint(0,3)

        # Ajout des déplacements possibles a une liste de choix
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

        # Séléction aléatoire du mouvement à effectuer
        if deplacement:
            dx, dy = random.choice(deplacement)
            pos[0]+=dx
            pos[1]+=dy
            # Vérifie si la case a déjà été visitée et ajoute 1 au nombre de cases visitées si ce n'est pas le cas
            if not(tuple(pos) in cases_visitees):
                cases_visitees.add(tuple(pos))
                nb_case_chemin+=1

            # Effectue le mouvement
            if direction == 0:
                barrieres[0][pos[1]][pos[0]-1] = 0
            elif direction == 1:
                barrieres[1][pos[0]][pos[1]-1] = 0

    return barrieres


def move(player_input : str, grille_sauvegarde : list, player_pos : list, new_map : list) -> tuple:
    """
    Permet le déplacement du joueur dans la carte à l'aide du mot de déplacement que l'on souhaite réaliser
    """
    assert type(grille_sauvegarde) == tuple, "la carte (grille_sauvegarde) n'est pas du bon type (doit être un tuple)"
    assert type(new_map) == tuple, "la carte (new_map) n'est pas du bon type (doit être un tuple)"
    assert type(player_pos) == list, "la position du joueur n'est pas du bon type (doit être une liste)"
    assert type(player_input) == str, "le player_input n'est pas du bon type (doit être une chaîne de caractères)"
    # Vérification du déplacement
    if player_input == 'gauche':
        if player_pos[1] == 0:
            print('Vous ne pouvez pas aller plus haut.')
        elif new_map[1][1][player_pos[0]][player_pos[1]-1] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            # Actualisation de la carte après le déplacement
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[1] -= 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'droite':
        if player_pos[1] == taille_carte[1]-1:
            print('Vous ne pouvez pas aller plus bas.')
        elif new_map[1][1][player_pos[0]][player_pos[1]] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            # Actualisation de la carte après le déplacement
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[1] += 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'haut':
        if player_pos[0] == 0:
            print('Vous ne pouvez pas aller plus à gauche.')
        elif new_map[1][0][player_pos[1]][player_pos[0]-1] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            # Actualisation de la carte après le déplacement
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[0] -= 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    elif player_input == 'bas':
        if player_pos[0] == taille_carte[0]-1:
            print('Vous ne pouvez pas aller plus à droite.')
        elif new_map[1][0][player_pos[1]][player_pos[0]] == 1:
            print('Vous êtes mort !')
            print('')
            # Réinitialisation de la carte et de la position du joueur après la mort
            new_map = copy.deepcopy(grille_sauvegarde)
            player_pos = [0, 0]
        else:
            # Actualisation de la carte après le déplacement
            new_map[0][player_pos[1]][player_pos[0]] = ' '
            player_pos[0] += 1
            new_map[0][player_pos[1]][player_pos[0]] = 'O'

    return new_map, player_pos

def jeux(taille_carte : list, fenetre, taille_fond : list)->tuple:
    """
    Fonction du jeux permettant les déplacements, la vérification du nombre de déchets restants, et de la mort du joueur
    """
    # Création de la position du joueur
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
    afficher_carte(taille_carte, grille[0], fenetre, taille_fond)

    for i in range(len(grille[0])):
        for k in grille[0][i]:
            if k != '*':
                case_sans_étoile += 1
            if case_sans_étoile == taille_carte[0]*taille_carte[1]:
                victoire()
                running = False

        case_sans_étoile = 0
    
    return grille, grille_sauvegarde, player_pos

pygame.init()



def creation_bouton(taille_bouton : tuple, color : tuple, texte : str, texte_color : tuple, bouton_pos : tuple)->list:
    '''
    cette fonction sert a creer un bouton
    '''
    assert type(taille_bouton) == tuple, 'surf devrait être un tuple'
    assert type(color) == tuple, 'color devrait être un tuple'
    assert type(texte) == str, 'texte devrait être un string'
    assert type(texte_color) == tuple, 'texte_color devrait être un tuple'
    assert type(bouton_pos) == tuple, 'bouton_pos devrait être un tuple'

    # Créer une police
    police = pygame.font.Font(None, 70)

    # Créé la surface du bouton
    bouton_surface = pygame.Surface(taille_bouton)
    # Colorise le bouton
    bouton_surface.fill(color)
    # Ajout du texte au bouton
    texte_bouton = police.render(texte, True, texte_color)
    position_texte = texte_bouton.get_rect(center=(taille_bouton[0]/2, taille_bouton[1]/2))
    bouton_surface.blit(texte_bouton, position_texte)
    # Récupère le rect du bouton pour s'en servir lors de son affichage
    bouton_rect = pygame.Rect(bouton_pos[0], bouton_pos[1], taille_bouton[0], taille_bouton[1])

    return [bouton_surface, taille_bouton, bouton_rect]

def actualisation_bouton(bouton, new_color : tuple, new_texte : str, new_texte_color : tuple):
    '''
    actualise la couleur et le texte du bouton
    '''
    assert type(new_color) == tuple, 'new_color devrait être un tuple'
    assert type(new_texte) == str, 'new_texte devrait être un string'
    assert type(new_texte_color) == tuple, 'new_texte_color devrait être un string'

    # Créer une police
    police = pygame.font.Font(None, 70)

    # Actualise la couleur du bouton
    bouton[0].fill(new_color)
    # Actualise le texte du bouton
    texte_bouton = police.render(new_texte, True, new_texte_color)
    position_texte = texte_bouton.get_rect(center=(bouton[1][0]/2, bouton[1][1]/2))
    # Affiche le bouton
    bouton[0].blit(texte_bouton, position_texte)

    return bouton[0]


def afficher_bouton(fenetre, bouton, bouton_pos : tuple, activation : bool):
    '''
    affiche le bouton
    '''
    assert type(bouton_pos) == tuple, 'bouton_pos devrait être un tuple'
    assert type(activation) == bool, 'activation devrait être un booléen'

    # Affiche le bouton sur la fenetre
    if activation:
        fenetre.blit(bouton, bouton_pos)


# Fonction qui affiche la carte
def afficher_carte(taille_carte : list, carte : list, fenetre, taille_fond : list):
    """
    Affiche la carte à l'écran
    """
    assert type(taille_carte) == list, 'Le paramètre taille_carte devrait être une liste'

    # Déchet
    dechet = pygame.image.load("dechet.png").convert()
    dechet.set_colorkey((255,255,255))

    # Sous-marin
    sous_marin = pygame.image.load("sousmarin.png").convert()
    sous_marin.set_colorkey((255, 255, 255))

    # Récupère les dimensions de l'objet et du sous marin
    taille_dechet = (dechet.get_width(), dechet.get_height())
    taille_sous_marin = (sous_marin.get_width(), sous_marin.get_height())

    # Création des dimensions de la surface invisible sur laquelle tous les objets seronts affichées en fonction du nombre d'objet et de la taille de l'écran pour simplifier l'affichage des objets a l'écran
    dimension_surface = (int(taille_fond[1]/taille_carte[1]), int(taille_fond[1]/taille_carte[1]))

    # Création d'une échelle pour le sous-marin et les déchets
    echelle_dechet = dimension_surface[0]/taille_dechet[1]
    echelle_sous_marin = dimension_surface[0]/taille_sous_marin[0]

    # Création d'un éspacement adaptatif entres les déchets et le sous-marin
    espacement_dechet = echelle_dechet * 10
    espacement_sous_marin = echelle_sous_marin * 10

    # Prise en compte de l'espacement adaptatif pour recalculer l'échelle des déchets et du sous-marin
    echelle_dechet = (dimension_surface[0] - (echelle_dechet * espacement_dechet * 2))/taille_dechet[1]
    echelle_sous_marin = (dimension_surface[0] - (echelle_sous_marin * espacement_sous_marin * 2))/ taille_sous_marin[0]

    # Mise à l'échelle des déchets et du sous-marin + récupération des nouvelles dimensions des objets
    dechet = pygame.transform.scale(dechet, (int(echelle_dechet * taille_dechet[0]), int(echelle_dechet * taille_dechet[1])))
    taille_dechet = (dechet.get_width(), dechet.get_height())
    sous_marin = pygame.transform.scale(sous_marin, (int(echelle_sous_marin * taille_sous_marin[0]), int(echelle_sous_marin * taille_sous_marin[1])))
    taille_sous_marin = (sous_marin.get_width(), sous_marin.get_height())

    # Création de la position des objets centrés dans la surface invisible
    dechet_pos = dechet.get_rect(center=(dimension_surface[0]/2, dimension_surface[1]/2))
    sous_marin_pos = sous_marin.get_rect(center=(dimension_surface[0]/2, dimension_surface[1]/2))

    # Affichage de tous les objets
    for k in range(taille_carte[1]):
        for i in range(taille_carte[0]):
            # Création des surfaces invisible
            surface = pygame.Surface(dimension_surface)
            surface.fill((0, 255, 0))
            surface.set_colorkey((0, 255, 0))
            # Centrage des surfaces pour faire apparaitre les objets au centre de l'écran
            centrage = taille_fond[0]/2 - (dimension_surface[0] * taille_carte[0])/2

            # Affichage de la carte. "*" pour déchet, "O" pour sous-marin
            if carte[i][k] == "*":
                # Ajout du déchet sur la surface
                surface.blit(dechet, dechet_pos)
                # Ajout de la surface sur la fenetre
                fenetre.blit(surface, (i * dimension_surface[0] + centrage, k * dimension_surface[1]))
            if carte[i][k] == "O":
                # Ajout du sous-marin à la surface
                surface.blit(sous_marin, sous_marin_pos)
                # Ajout de la surface sur la fenetre
                fenetre.blit(surface, (i * dimension_surface[0] + centrage, k * dimension_surface[1]))


def victoire():
    '''
    Fonction qui s'active quand le joueurs a gagné
    '''
    pass

# Création de la fenetre
fenetre = pygame.display.set_mode((0,0),FULLSCREEN)
# Récupère les dimensions de l'écran
rec = fenetre.get_size()

# Création de la taille de la carte et assignation à [2, 2]
taille_carte = [2,2]

# Chargement du fond
fond = pygame.image.load("fond_de_jeu.jpg").convert()

# Ajuste la taille du fond à l'écran
fond = pygame.transform.scale(fond, (rec[0], rec[1]))

# Récupération des dimensions du fond
dimension_fondx = fond.get_width()
dimension_fondy = fond.get_height()

position_fond = (0, 0)
fenetre.blit(fond, position_fond)

# Créer une police de titre
police = pygame.font.Font(None, 200)

# Variables de visibilités des boutons
boutons_menu_principal_activation = True
boutons_menu_creatif_activation = False

# bouton créatif
bouton_creatif = creation_bouton((500, 100), (100, 100, 100), 'Mode Créatif', (255, 255, 255), (dimension_fondx/2-250, dimension_fondy/2+400))
bouton_creatif_activation = True

# bouton affichage taille carte
bouton_taille_carte = creation_bouton((500, 100), (100, 100, 100), str(taille_carte), (255, 255, 255), (dimension_fondx/2-250, dimension_fondy/2+400))
bouton_taille_carte_activation = False

# bouton augmenter
bouton_augmenter = creation_bouton((100, 45), (100, 100, 100), '+', (255, 255, 255), (dimension_fondx/2+260, dimension_fondy/2+400))
bouton_augmenter_activation = False

# bouton diminuer
bouton_diminuer = creation_bouton((100, 45), (100, 100, 100), '-', (255, 255, 255), (dimension_fondx/2+260, dimension_fondy/2+455))
bouton_diminuer_activation = False

# Bouton valider
bouton_valider = creation_bouton((200, 100), (100, 100, 100), 'Valider', (255, 255, 255), (dimension_fondx/2+370, dimension_fondy/2+400))
bouton_valider_activation = False

# Bouton Menu Principal
bouton_menu = creation_bouton((200, 100), (100, 100, 100), 'Menu', (255, 255, 255), (100, dimension_fondy/2+400))
bouton_menu_activation = False

# Titre
titre_activation = True

# Bouton Facile
bouton_facile = creation_bouton((500, 100), (100, 100, 100), 'Facileeeeeee', (255, 255, 255), (dimension_fondx/2-250, dimension_fondy/2-200))
bouton_facile_activation = True

# Bouton Normal
bouton_normal = creation_bouton((500, 100), (100, 100, 100), 'THE game', (255, 255, 255), (dimension_fondx/2-250, dimension_fondy/2-75))
bouton_normal_activation = True

# Bouton Hard
bouton_hard = creation_bouton((500, 100), (100, 100, 100), 'Tu veux mourir?', (255, 255, 255), (dimension_fondx/2-250, dimension_fondy/2+50))
bouton_hard_activation = True

# Variable indiquant si le jeux a commencé
jeux_activation = False

# Création de la variable de position du joueurs
player_pos = [0, 0]

continuer = True

while continuer:

    for event in pygame.event.get():
        
        # Quitter le Jeux
        if event.type == QUIT:
            continuer = False

        elif event.type == KEYDOWN:
            
            # Quitter le Jeux
            if event.key == K_ESCAPE:
                continuer = False
            
            # Mouvements du personnage
            if event.key == K_LEFT:
                fenetre.blit(fond, position_fond)
                if jeux_activation:
                    # Actualisation de la carte
                    carte, player_pos = move('gauche', jeux_info[1], player_pos, carte)
                    # Affichage de la carte
                    afficher_carte(taille_carte, carte[0], fenetre, [dimension_fondx, dimension_fondy])
            
            if event.key == K_RIGHT:
                fenetre.blit(fond, position_fond)
                if jeux_activation:
                    # Actualisation de la carte
                    carte, player_pos = move('droite', jeux_info[1], player_pos, carte)
                    # Affichage de la carte
                    afficher_carte(taille_carte, carte[0], fenetre, [dimension_fondx, dimension_fondy])
            
            if event.key == K_UP:
                fenetre.blit(fond, position_fond)
                if jeux_activation:
                    # Actualisation de la carte
                    carte, player_pos = move('haut', jeux_info[1], player_pos, carte)
                    # Affichage de la carte
                    afficher_carte(taille_carte, carte[0], fenetre, [dimension_fondx, dimension_fondy])
            
            if event.key == K_DOWN:
                fenetre.blit(fond, position_fond)
                if jeux_activation:
                    # Actualisation de la carte
                    carte, player_pos = move('bas', jeux_info[1], player_pos, carte)
                    # Affichage de la carte
                    afficher_carte(taille_carte, carte[0], fenetre, [dimension_fondx, dimension_fondy])

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # Vérifie si le bouton_creatif est cliqué
                if bouton_creatif[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_principal_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_creatif_activation = True
                        boutons_menu_principal_activation = False

                # Vérifie si le bouton_augmenter est cliqué
                elif bouton_augmenter[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_creatif_activation:
                        taille_carte[0], taille_carte[1] = taille_carte[0]+1, taille_carte[1]+1

                # Vérifie si le bouton_diminuer est cliqué
                elif bouton_diminuer[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_creatif_activation:
                        if taille_carte[0] != 2:
                            taille_carte[0], taille_carte[1] = taille_carte[0]-1, taille_carte[1]-1

                # Vérifie si le bouton_valider est cliqué
                elif bouton_valider[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_creatif_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_creatif_activation = False
                        # Lancement du Jeux
                        jeux_activation = True

                # Vérifie si le bouton_menu est cliqué
                elif bouton_menu[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_creatif_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_principal_activation = True
                        boutons_menu_creatif_activation = False

                # Vérifie si le bouton_facile est cliqué
                elif bouton_facile[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_principal_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_principal_activation = False
                        # Lancement du Jeux
                        jeux_activation = True
                        taille_carte = [3, 3]

                # Vérifie si le bouton_normal est cliqué
                elif bouton_normal[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_principal_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_principal_activation = False
                        # Lancement du Jeux
                        jeux_activation = True
                        taille_carte = [5, 5]

                # Vérifie si le bouton_hard est cliqué
                elif bouton_hard[2].collidepoint(pygame.mouse.get_pos()):
                    # Vérifie que le bouton peut être cliqué
                    if boutons_menu_principal_activation:
                        fenetre.blit(fond, position_fond)
                        boutons_menu_principal_activation = False
                        # Lancement du Jeux
                        jeux_activation = True
                        taille_carte = [7, 7]


            # Lancement du Jeux
            if jeux_activation:
                jeux_info = jeux(taille_carte, fenetre, [dimension_fondx, dimension_fondy])
                carte = jeux_info[0]


    # bouton créatif
    afficher_bouton(fenetre, bouton_creatif[0], (dimension_fondx/2-250, dimension_fondy/2+400), boutons_menu_principal_activation)

    # bouton taille_carte
    bouton_taille_carte[0] = actualisation_bouton(bouton_taille_carte, (100, 100, 100), str(taille_carte), (255, 255, 255))
    afficher_bouton(fenetre, bouton_taille_carte[0], (dimension_fondx/2-250, dimension_fondy/2+400), boutons_menu_creatif_activation)

    # Bouton augmenter
    afficher_bouton(fenetre, bouton_augmenter[0], (dimension_fondx/2+260, dimension_fondy/2+400), boutons_menu_creatif_activation)

    # Bouton diminuer
    afficher_bouton(fenetre, bouton_diminuer[0], (dimension_fondx/2+260, dimension_fondy/2+455), boutons_menu_creatif_activation)

    # Bouton valider
    afficher_bouton(fenetre, bouton_valider[0], (dimension_fondx/2+370, dimension_fondy/2+400), boutons_menu_creatif_activation)

    # Bouton Menu
    afficher_bouton(fenetre, bouton_menu[0], (100, dimension_fondy/2+400), boutons_menu_creatif_activation)

    # Bouton Facile
    afficher_bouton(fenetre, bouton_facile[0], (dimension_fondx/2-250, dimension_fondy/2-200), boutons_menu_principal_activation)

    # Bouton Normal
    afficher_bouton(fenetre, bouton_normal[0], (dimension_fondx/2-250, dimension_fondy/2-75), boutons_menu_principal_activation)

    # Bouton Hard
    afficher_bouton(fenetre, bouton_hard[0], (dimension_fondx/2-250, dimension_fondy/2+50), boutons_menu_principal_activation)

    # Affichage du titre
    if boutons_menu_principal_activation:
        #titre
        titre = police.render("Sous-MarinThe", True, (255, 255, 255))
        position_titre = titre.get_rect(center=(dimension_fondx/2, 100))
        fenetre.blit(titre, position_titre)

    pygame.display.flip()

pygame.quit()