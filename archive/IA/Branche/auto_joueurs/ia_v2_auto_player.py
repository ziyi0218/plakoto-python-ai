import random
import copy
from datetime import datetime
import builtins
import sys

random.seed(3)

#######################################################################################
# 3 avril rzy (v1_auto players)
# Redéfinition de la fonction main

# 5 avril rzy (v2)
# Redéfinition de la fonction "check_victoire"

'''
############################## INPUT ####################################################
#----Cette partie est utilisée pour générer automatiquement le fichier input---#
seed_value = 1

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
filename = f"Ziyi_inputs_{timestamp}_SEED_{seed_value}.txt"
log_file = open(filename, "w")
original_input = builtins.input


def custom_input(prompt=""):
    value = original_input(prompt)
    log_file.write(value + "\n")
    log_file.flush()
    return value


builtins.input = custom_input

#---------------- input-enter----------------------#

input_file = open(r"D:\Code\Python\S4_L2N1\Interface textuelle\Trunk\inputs_seed1\input_seed1_full_test.txt", "r")
original_input = builtins.input

def custom_input_enter(prompt=""):
    print(prompt, end="")
    value = input_file.readline()
    if not value:
        # Fin du fichier : repasser à input normal
        print("\n[Fin du fichier d'entrée — passage à la saisie manuelle]")
        builtins.input = original_input
        return original_input(prompt)
    value = value.rstrip("\n")
    print(value)
    return value

builtins.input = custom_input_enter
'''

############################ CREATION DU PLATEAU ############################################
def init_plateau():
    """
    Initialiser le plateau et placer les pièces de départ.
    Ajout de compteurs pour suivre le nombre de pions sortis (off) pour B et N.
    Entrée:
      - Aucune
    Sortie:
      - dict[int, list[str]] : Un dictionnaire où chaque clé (0..23) correspond à une case
        et la valeur est une liste de pions ("B" ou "N").
    """
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)  # 15 pions blancs (B)
    plateau[23] = list("N" * 15)  # 15 pions noirs (N)
    plateau["off_B"] = 0  # Nombre de pions blancs sortis
    plateau["off_N"] = 0  # Nombre de pions noirs sortis
    return plateau


############################ AFFICHAGE DU PLATEAU (SIMPLIFIE) ############################################
def afficher_plateau(plateau):
    """
    Affichage ASCII simplifié du plateau + info sur pions déjà sortis.
    """
    print("\n" + "=" * 49)
    print(" " * 17 + "PLATEAU PLAKOTO")
    print("=" * 49 + "\n")
    print(f"(Sortis) B: {plateau['off_B']} | N: {plateau['off_N']}\n")

    cells = []
    for i in range(24):
        count = len(plateau[i]) if isinstance(plateau[i], list) else 0
        if count == 0:
            cells.append((0, ' '))
        else:
            symbol = plateau[i][-1]
            cells.append((count, symbol))

    haut = cells[:12]
    bas = cells[12:]

    # Affichage de la partie supérieure (selon la pièce du dessus)
    for i in range(6, 0, -1):
        ligne = "|"
        for cell in reversed(haut):
            count, symbol = cell
            if i == 6 and count > 5:
                ligne += f"+{count - 5}{symbol}|"
            elif count > i:
                ligne += f" {symbol} |"
            else:
                ligne += "   |"
        print(ligne)

    # Affichage de la ligne des pièces du bas de la case pour la moitié supérieure
    # On utilise ici les indices internes 11 à 0 (correspondant aux positions externes 12 à 1)
    print("| " + " | ".join(
          plateau[i][0] if plateau[i] else " "
          for i in range(11, -1, -1)
         ) + " |")

    # Affichage de la ligne de numérotation pour la moitié supérieure
    print("|" + " |".join(f"{i:2}" for i in range(12, 0, -1)) + " |")
    print("|" + "---|" * 12)
    # Affichage de la ligne de numérotation pour la moitié inférieure
    print("|" + " |".join(f"{i:2}" for i in range(13, 25)) + " |")

    # Affichage de la ligne des pièces du bas de la case pour la moitié inférieure
    # On utilise ici les indices internes 12 à 23 (correspondant aux positions externes 13 à 24)
    print("| " + " | ".join(
          plateau[i][0] if plateau[i] else " "
          for i in range(12, 24)
         ) + " |")

    # Affichage de la partie inférieure (selon la pièce du dessus)
    for i in range(1, 7):
        ligne = "|"
        for cell in bas:
            count, symbol = cell
            if i == 6 and count > 5:
                ligne += f"+{count - 5}{symbol}|"
            elif count > i:
                ligne += f" {symbol} |"
            else:
                ligne += "   |"
        print(ligne)



############################ LANCEMENT DES DÉS ############################################
def lance_de():
    """
    Simuler le lancer de deux dés.
    Si c'est un double, renvoyer 4 fois la même valeur, sinon renvoyer les deux valeurs.

    Entrée:
      - Aucune
    Sortie:
      - list[int] : Liste des valeurs de dés (ex: [3,4] ou [6,6,6,6] pour un double).
    """
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    if d1 == d2:
        return [d1] * 4  # Double : peut être joué 4 fois
    else:
        return [d1, d2]


############################ COMMANDE DE JEU ##############################################
def afficher_commandes():
    """
    Afficher la liste des commandes disponibles.

    Entrée:
      - Aucune
    Sortie:
      - Aucune (affichage console)
    """
    print("\nCommandes disponibles :")
    print("  help                      -> Afficher la liste des commandes")
    print("  lance                     -> Lancer les dés")
    print("  plateau                   -> Afficher le plateau")
    print("  move <origine> <destination>  -> Déplacer un pion")
    print("  quit                      -> Quitter le jeu")


############################ VERIFICATION DE DEPLACEMENT ####################################
def is_move_legal_by_dice(origine, destination, dice, joueur):
    """
    Vérifier si le déplacement est légal en fonction des valeurs des dés.
    Hypothèses :
      - Pour les pions blancs (B), le mouvement doit se faire d'un indice plus petit à un indice plus grand,
        et la distance doit correspondre à l'une des valeurs du dé.
      - Pour les pions noirs (N), le mouvement doit se faire d'un indice plus grand à un indice plus petit.

    Entrée:
      - origine: int
      - destination: int
      - dice: list[int]
      - joueur: str ("B" ou "N")
    Sortie:
      - bool : True si le déplacement est légal, False sinon.
    """
    move_distance = abs(destination - origine)
    if move_distance in dice:
        if joueur == "B" and destination > origine:
            return True
        if joueur == "N" and origine > destination:
            return True
    return False


############################ HOME BOARD & BEARING OFF ######################################
def in_home_board(pos, joueur):
    """
    Vérifie si la position pos est dans la zone "home board" du joueur.
    Ex: pour B, home board = 18..23; pour N, home board = 0..5
    (Vous pouvez ajuster selon vos règles.)
    
    Entrée:
      - pos: int
      - joueur: str ("B" ou "N")
    Sortie:
      - ?
    
    """
    if joueur == "B":
        return 18 <= pos <= 23
    return 0 <= pos <= 5

def all_in_home(plateau, joueur):
    """
    Vérifie si le joueur a tous ses pions dans sa home board,
    en tenant compte de la possibilité qu'ils soient sous un pion adverse.
    """

    for i in range(24):
        if plateau[i]:
            for pion in plateau[i]:
                if pion == joueur and not in_home_board(i, joueur):
                        return False
    return True

def bearing_off_possible(plateau, origine, dice_value, joueur):
    """
    Vérifie si on peut sortir le pion situé en 'origine' avec le dé = dice_value.
    Règles:
      - Tous les pions du joueur doivent être dans la home board.
      - Si dice_value == distance, OK.
      - Si dice_value > distance, alors vérifier s'il n'existe pas de pion plus éloigné.
    """
    if not all_in_home(plateau, joueur):
        return False

    # Calcul de la "distance" vers la sortie
    if joueur == "B":
        distance = 24 - origine
    else:  # joueur == "N"
        distance = origine - (-1)

    if dice_value == distance:
        return True
    elif dice_value > distance:
        # Vérifier s'il existe un pion plus éloigné
        return not existe_pion_plus_lointain(plateau, joueur, origine)
    else:
        return False

def existe_pion_plus_lointain(plateau, joueur, origine):
    if joueur == 'B':
        for i in range(origine - 1, 17, -1):  # de (origine -1) à 18 inclus
            if in_home_board(i, joueur) and plateau[i] and joueur in plateau[i]:
                return True
    else:  # joueur == 'N'
        for i in range(origine + 1, 6):  # de (origine +1) à 5 inclus
            if in_home_board(i, joueur) and plateau[i] and joueur in plateau[i]:
                return True
    return False

def bearing_off(plateau, origine, joueur):
    """
    Retire le pion de la case 'origine' du plateau et incrémente le compteur off_B/off_N.
    """
    plateau[origine].pop()
    if joueur == "B":
        plateau["off_B"] += 1
    else:
        plateau["off_N"] += 1


############################ DEPLACEMENT DE PION ############################################
def deplacer_pion(plateau, origine, destination, joueur):
    """
    Déplacer une pièce selon les règles de base :
      - Vérifier que la case d'origine contient une pièce appartenant au joueur.
      - Si la case de destination contient déjà des pièces, vérifier si le déplacement est autorisé
        (si la case est occupée par plus d'une pièce adverse, le déplacement est interdit)
      - Tente de déplacer un pion. Si 'destination' est en dehors (ex: 24 pour B, ou -1 pour N),
    on vérifie si c'est un coup de bearing off.

    Entrée:
      - plateau: dict[int, list[str]]
      - origine: int
      - destination: int
      - joueur: str ("B" ou "N")
    Sortie:
      - bool : True si le déplacement s'est effectué, False sinon.
    """

    if not plateau[origine]:
        print("Erreur : la case d'origine est vide.")
        return False

    if plateau[origine][-1] != joueur:
        print("Erreur : la pièce à la case d'origine ne vous appartient pas.")
        return False

    # Cas : bearing off (sortir le pion) ?
    # Ex: pour B, si destination == 24 => on veut sortir
    #     pour N, si destination == -1 => on veut sortir
    if joueur == "B" and destination == 24:
        dist = 24 - origine
        # On suppose qu'on a un dé >= dist
        # On doit vérifier bearing_off_possible
        # => Si OK, on sort le pion
        if bearing_off_possible(plateau, origine, dist, "B"):
            plateau[origine].pop()
            plateau["off_B"] += 1
            return True
        return False
    if joueur == "N" and destination == -1:
        dist = origine - (-1)
        if bearing_off_possible(plateau, origine, dist, "N"):
            plateau[origine].pop()
            plateau["off_N"] += 1
            return True
        return False

    # Cas normal : on vérifie la destination
    if destination < 0 or destination > 23:
        # Ce n'est pas un move standard ni un bearing off correct
        return False

    if plateau[destination]:
        if plateau[destination][-1] != joueur:
            if len(plateau[destination]) > 1:
                return False
            # elif len(plateau[destination]) == 1:
            #    pass # Bloquer ou autre
    piece = plateau[origine].pop()
    plateau[destination].append(piece)
    return True


############################ CONDITION DE VICTOIRE #########################################
def check_victoire(plateau, joueur):
    """
    Vérifier si le joueur a gagné en sortant tous ses pions.
    On regarde plateau["off_B"] ou plateau["off_N"] == 15.

    Entrée:
      - plateau: dict[int, list[str]]
      - joueur: str ("B" ou "N")
    Sortie:
      - bool : True si le joueur a gagné, False sinon.
    """
    if joueur == "B":
        if plateau[23] and plateau[23][0] == "N" and plateau[23][-1] != "N":
            return True 
        return plateau["off_B"] == 15
    else:  # joueur == "N"
        if plateau[0] and plateau[0][0] == "B" and plateau[0][-1] != "B":
            return True 
        return plateau["off_N"] == 15

####################### GÉNÉRATION DES MACRO COUPS #########################################
def get_movable_pieces(board, joueur):
    """
    Retourner la liste des indices où le joueur peut déplacer une pièce,
    c'est-à-dire les cases non vides dont la pièce du dessus appartient au joueur.

    Entrée:
      - board: dict[int, list[str]]
      - joueur: str ("B" ou "N")
    Sortie:
      - list[int] : Liste des indices (0..23) où le joueur possède la pièce du dessus.
    """
    indices = []
    for i in range(24):
        if board[i] and board[i][-1] == joueur:
            indices.append(i)
    return indices


def simulate_move(board, origine, destination, joueur):
    """
    Simuler le déplacement d'une pièce sans modifier le plateau original.
    Retourne une copie du plateau après déplacement.

    Entrée:
      - board: dict[int, list[str]]
      - origine: int
      - destination: int
      - joueur: str ("B" ou "N")
    Sortie:
      - dict[int, list[str]] ou None : Copie du plateau modifiée, ou None si le déplacement échoue.
    """
    new_board = copy.deepcopy(board)
    if deplacer_pion(new_board, origine, destination, joueur):
        return new_board
    return None


def board_signature(board):
    """
    Générer une signature du plateau sous forme de chaîne de caractères,
    qui résume l'état final du plateau.
    Inclure aussi le nombre de pions sortis dans la signature.

    Entrée:
      - board: dict[int, list[str]]
    Sortie:
      - str : Représentation textuelle du plateau (toutes les cases concaténées).
    """
    main_part = '|'.join(''.join(board[i]) for i in range(24))
    off_part = f"Boff={board['off_B']},Noff={board['off_N']}"
    return main_part + "|" + off_part


def generate_macro_moves(board, dice, current_player):
    """
    Génère tous les macro-coups possibles à partir de l'état actuel du plateau,
    des dés disponibles et du joueur courant.

    Entrées :
      - board : dict[int, list[str]]
          Le plateau de jeu, chaque clé (0 à 23) représente une case, et la valeur est
          une liste de pions ('B' ou 'N'). Les clés spéciales "off_B" et "off_N" représentent
          le nombre de pions sortis pour chaque joueur.

      - dice : list[int]
          Liste des dés disponibles à ce tour (ex: [3, 4] ou [6, 6, 6, 6] pour un double).

      - current_player : str
          Le joueur en cours, soit "B" (blanc) ou "N" (noir).

    Sortie :
      - dict[str, list[list[tuple[int, int, int]]]]
          Un dictionnaire dont :
            - les clés sont des signatures uniques d’états finaux de plateau (str),
            - les valeurs sont des listes de macro-coups,
              chaque macro-coup étant une liste de micro-coups (tuple origine, destination, valeur_du_dé).

          Exemple d’un élément :
          {
            '...|Boff=3,Noff=2': [
                [(0, 3, 3), (5, 8, 3)],
                [(0, 4, 4)]
            ]
          }
    """
    if not dice:
        sig = board_signature(board)
        return {sig: [[]]}

    macro_moves = {}
    movable = get_movable_pieces(board, current_player)

    if not movable:
        sig = board_signature(board)
        return {sig: [[]]}

    for origine in movable:
        for d in dice:
            if current_player == "B":
                destination = origine + d
            else:
                destination = origine - d

            if current_player == "B" and all_in_home(board, "B") and destination > 23:
                destination = 24
            if current_player == "N" and all_in_home(board, "N") and destination < 0:
                destination = -1

            new_board = simulate_move(board, origine, destination, current_player)
            if new_board is None:
                continue

            new_dice = dice.copy()
            try:
                new_dice.remove(d)
            except ValueError:
                continue

            subsequent_moves = generate_macro_moves(new_board, new_dice, current_player)
            if not subsequent_moves:
                sig = board_signature(new_board)
                macro_moves.setdefault(sig, []).append([(origine, destination, d)])
            else:
                for sig, moves_list in subsequent_moves.items():
                    for moves in moves_list:
                        full_move = [(origine, destination, d)] + moves
                        macro_moves.setdefault(sig, []).append(full_move)

    return macro_moves


############################## MAX PRATIQUE ###############################################
def score_macro_move(macro_move):
    """
    Calcule la somme des distances de tous les micro coups, y compris bearing off.
    Ex: (origine, destination, d).
    - Si c'est un bearing off pour B => (origine,24), distance = 23-origine
    - Pour N => (origine,-1), distance = origine-0
    - Sinon => abs(destination-origine)
    """
    total = 0
    for (o, dest, d) in macro_move:
        if dest == 24:  # B sort
            total += (24 - o)
        elif dest == -1:  # N sort
            total += o + 1
        else:
            total += abs(dest - o)
    return total

def filter_max_pratique(macro_dict):
    """
    macro_dict : { signature: [ [ (o,d,val), (o2,d2,val2),...], ... ] }
    On calcule le score de chaque macro coup, on trouve le max, on ne garde que ceux = max.
    """
    filtered_dict = {}
    max_score_global = 0

    # 1) Trouver le score max
    for sig, coups in macro_dict.items():
        for coup in coups:
            s = score_macro_move(coup)
            if s > max_score_global:
                max_score_global = s

    # 2) Filtrer
    for sig, coups in macro_dict.items():
        best_coups = []
        for coup in coups:
            s = score_macro_move(coup)
            if s == max_score_global:
                best_coups.append(coup)
        if best_coups:
            filtered_dict[sig] = best_coups

    return filtered_dict

def is_move_prefix_in_macro_moves(board, dice, current_player, player_move):
    """
    Vérifie si un micro-coup proposé (player_move) est valide dans le contexte du plateau et des dés actuels.

    Le coup est considéré valide si :
      - Il correspond au premier mouvement d’un macro-coup optimal (filtré via Max Pratique),
      - Ou bien, il correspond au premier mouvement d’un macro-coup légal (même s’il n’est pas optimal),
      - Ou enfin, il est simulable directement sur le plateau et respecte la logique des dés et du bearing off.

    Entrées :
      - board : dict[int, list[str]]
          Le plateau de jeu, chaque clé (0 à 23) représente une case, et la valeur est
          une liste de pions ('B' ou 'N'). Les clés spéciales "off_B" et "off_N" indiquent
          le nombre de pions sortis pour chaque joueur.

      - dice : list[int]
          Liste des dés restants à jouer pour ce tour (ex : [2, 4]).

      - current_player : str
          Le joueur en cours : "B" (blanc) ou "N" (noir).

      - player_move : tuple[int, int, int]
          Un micro-coup candidat à valider, de la forme :
          (origine, destination, valeur_du_dé)

          Par exemple : (20, 24, 5) représente une sortie d’un pion blanc de la case 21 avec un dé de 5.

    Sortie :
      - bool
          True si le coup est reconnu comme valide dans les conditions actuelles (optimal ou acceptable),
          False s’il est rejeté (non conforme, non simulable ou sans correspondance dans les coups légaux).
    """

    macro_moves = generate_macro_moves(board, dice, current_player)
    filtered = filter_max_pratique(macro_moves)

    move_found = False

    # Priorité : est-ce un coup parmi les meilleurs ?
    for sig, moves_list in filtered.items():
        for move_seq in moves_list:
            if len(move_seq) >= 1 and move_seq[0] == player_move:
                return True  # Optimal = on accepte

    # Sinon, vérifier s’il est au moins présent dans les coups légaux
    for sig, moves_list in macro_moves.items():
        for move_seq in moves_list:
            if len(move_seq) >= 1 and move_seq[0] == player_move:
                print("(Info : coup autorisé car légal mais pas optimal.)")
                return True

    # Dernier secours : simuler le coup directement
    origine, destination, dist = player_move
    if dist not in dice:
        return False

    if destination == 24 or destination == -1:
        return bearing_off_possible(board, origine, dist, current_player)

    simulated = simulate_move(board, origine, destination, current_player)
    filtered = filter_max_pratique(macro_moves)

    move_found = False

    # Priorité : est-ce un coup parmi les meilleurs ?
    for sig, moves_list in filtered.items():
        for move_seq in moves_list:
            if len(move_seq) >= 1 and move_seq[0] == player_move:
                return True  # Optimal = on accepte

    # Sinon, vérifier s’il est au moins présent dans les coups légaux
    for sig, moves_list in macro_moves.items():
        for move_seq in moves_list:
            if len(move_seq) >= 1 and move_seq[0] == player_move:
                move_found = True  # Coup non optimal mais permis

    if move_found:
        print("(Info : coup autorisé car légal mais pas optimal.)")
        return True

    # Dernier secours : simuler le coup directement
    origine, destination, dist = player_move
    if dist not in dice:
        return False

    if destination == 24 or destination == -1:
        return bearing_off_possible(board, origine, dist, current_player)

    simulated = simulate_move(board, origine, destination, current_player)
    return simulated is not None

############################ GESTION DES COMMANDES ##########################################
def gestion_commande(cmd, plateau, joueur, dice):
    """
    Traiter la commande entrée par l'utilisateur et retourner un tuple :
    (continuer le jeu, déplacement effectué, dés restants).

    Entrée:
      - cmd: str (commande utilisateur, ex: "move 1 5")
      - plateau: dict[int, list[str]]
      - joueur: str ("B" ou "N")
      - dice: list[int] (dés restants pour ce tour)
    Sortie:
      - tuple[bool, bool, list[int]] :
        (continuer_le_jeu, deplacement_effectue, des_restants)
    """
    if cmd == "help":
        afficher_commandes()
        return True, False, dice

    elif cmd == "lance":
        if dice:
            print("Vous avez déjà lancé les dés pour ce tour, veuillez directement effectuer un déplacement.")
            return True, False, dice
        new_dice = lance_de()
        print("Résultat des dés :", new_dice)
        return True, False, new_dice

    elif cmd == "plateau":
        afficher_plateau(plateau)
        return True, False, dice

    elif cmd == "quit":
        print("Fin du jeu, au revoir !")
        return False, False, dice

    elif cmd.startswith("move"):
        parts = cmd.split()
        if len(parts) != 3:
            print("Erreur de format de commande. Usage correct : move <origine> <destination>")
            return True, False, dice
        try:
            origine = int(parts[1]) - 1
            destination = int(parts[2]) - 1
        except ValueError:
            print("Erreur : la position doit être un chiffre.")
            return True, False, dice

        # Détermination brute de move_distance en recherchant le dé possible
        if joueur == "B" and destination > 23 and all_in_home(plateau, "B"):
            destination = 24
        if joueur == "N" and destination < 0 and all_in_home(plateau, "N"):
            destination = -1

        # Maintenant on déduit le move_distance à partir du dé disponible
        move_distance = None
        for d in dice:
            if joueur == "B" and destination == 24:
                if bearing_off_possible(plateau, origine, d, joueur):
                    move_distance = d
                    break
            elif joueur == "N" and destination == -1:
                if bearing_off_possible(plateau, origine, d, joueur):
                    move_distance = d
                    break
            elif abs(destination - origine) == d:
                move_distance = d
                break

        if move_distance is None:
            print("Erreur : Aucun dé ne correspond à ce mouvement.")
            return True, False, dice

        player_move = (origine, destination, move_distance)

        # Vérifier max pratique
        if not is_move_prefix_in_macro_moves(plateau, dice, joueur, player_move):
            print("Erreur : ce micro coup n'est pas valide.")
            return True, False, dice

        # Tenter le déplacement
        if deplacer_pion(plateau, origine, destination, joueur):
            print(f"Le joueur {joueur} a déplacé avec succès.")
            # Retirer la valeur du dé (distance ou bearing off())
            try:
                dice.remove(move_distance)
            except ValueError:
                pass
            return True, True, dice
        else:
            print("Déplacement échoué.")
            return True, False, dice

    else:
        print("Commande inconnue. Veuillez taper 'help' pour afficher la liste des commandes.")
        return True, False, dice
    
def peut_jouer_au_moins_un_de(plateau, dice, joueur):
    for d in dice:
        for origine in get_movable_pieces(plateau, joueur):
            dest = origine + d if joueur == "B" else origine - d

            # Gestion du bearing off correct
            if joueur == "B" and all_in_home(plateau, "B") and dest > 23:
                dest = 24
            elif joueur == "N" and all_in_home(plateau, "N") and dest < 0:
                dest = -1

            if simulate_move(plateau, origine, dest, joueur) is not None:
                return True
    return False

############################ MAIN DU JEU ############################################
def main_auto():
    """
    Fonction principale pour simuler un match entre deux joueurs aléatoires, avec des conditions 
    pour éviter les boucles infinies.
    À chaque tour, le joueur courant :
      - Lance les dés et affiche le résultat,
      - Génère tous les macro coups possibles à partir du plateau actuel,
      - Sélectionne aléatoirement un coup parmi les coups disponibles et l'affiche,
      - Exécute le coup (chaque micro coup) et met à jour le plateau,
      - Vérifie si le joueur a gagné.
    Si aucun coup n'est possible ou si aucun progrès (aucune valeur de dé consommée) est réalisé 
    pendant plusieurs tours consécutifs, le tour se termine et on passe au joueur adverse.
    Un maximum de tours est également imposé pour éviter une boucle infinie.
    """
    # Initialisation du plateau et affichage initial
    plateau = init_plateau()
    print("Plateau initial :")
    afficher_plateau(plateau)
    
    # Le joueur blanc commence
    current_player = "B"
    
    # Paramètres de sécurité
    max_turns = 7       # Nombre maximum de tours autorisés
    turn_count = 0
    no_progress_global = 0  # Compteur de tours sans aucun progrès
    
    # Boucle principale
    while turn_count < max_turns:
        turn_count += 1
        print("\n=== Tour {} : Joueur {} ===".format(turn_count, current_player))
        
        # Lancer les dés pour ce tour et afficher le résultat
        dice = lance_de()
        print("Résultat des dés :", dice)
        
        progress_this_turn = False  # Marque si au moins un dé est consommé dans ce tour
        
        # Boucle interne : tant qu'il reste des dés jouables
        while dice:
            progress = False  # Marque si un dé est consommé dans cette itération

            # Générer tous les macro coups possibles pour la configuration actuelle
            macro_moves = generate_macro_moves(plateau, dice, current_player)
            available_moves = []
            for moves_list in macro_moves.values():
                available_moves.extend(moves_list)
            
#——————————————————————————————————————————————————————————————————————————————————————————————
            print("Tous les coups:")
            for signature, moves in macro_moves.items():
                print(f"{signature} : {moves}")

#——————————————————————————————————————————————————————————————————————————————————————————————
            # Si aucun coup n'est possible, sortir de la boucle de ce tour
            if not available_moves:
                print("Aucun coup possible pour le joueur {} avec les dés {}.".format(current_player, dice))
                break
            
            # Sélection aléatoire d'un coup parmi les coups disponibles
            chosen_move = random.choice(available_moves)
            # Si le coup choisi est vide, on force la fin du tour
            if not chosen_move:
                print("Le coup choisi est vide, fin du tour pour le joueur {}.".format(current_player))
                break
            
            print("Coup choisi par le joueur {} : {}".format(current_player, chosen_move))
            
            # Exécuter la séquence de micro coups du coup choisi
            for micro_coup in chosen_move:
                origine, destination, valeur_de = micro_coup
                if deplacer_pion(plateau, origine, destination, current_player):
                    # Préparation de l'affichage de la destination
                    if destination == 24:
                        affichage_dest = "sortie (24)"
                    elif destination == -1:
                        affichage_dest = "sortie (-1)"
                    else:
                        affichage_dest = str(destination + 1)
                    print("Joueur {} : déplacement de la case {} à la case {} avec le dé {}."
                          .format(current_player, origine + 1, affichage_dest, valeur_de))
                    
                    # Retirer le dé utilisé et marquer le progrès
                    try:
                        dice.remove(valeur_de)
                        progress = True
                        progress_this_turn = True
                    except ValueError:
                        print("Erreur : le dé {} n'a pas pu être retiré.".format(valeur_de))
                    
                    # Afficher l'état du plateau après le déplacement
                    afficher_plateau(plateau)
                    
                    # Vérifier immédiatement la victoire
                    if check_victoire(plateau, current_player):
                        print("Le joueur {} a gagné !".format(current_player))
                        return
                else:
                    print("Erreur lors de l'exécution du micro coup :", micro_coup)
                    # En cas d'erreur sur un micro coup, interrompre l'exécution du coup choisi
                    break
            
            # Si aucun dé n'a été consommé dans cette itération, on force la fin du tour
            if not progress:
                print("Aucun dé consommé dans cette itération, fin du tour pour le joueur {}.".format(current_player))
                break
            
            # Si aucun coup supplémentaire n'est possible avec les dés restants, sortir de la boucle interne
            if not dice or not peut_jouer_au_moins_un_de(plateau, dice, current_player):
                break
        
        print("Fin du tour du joueur {}. Dés restants à la fin du tour : {}.".format(current_player, dice))
        
        # Si aucun progrès n'est réalisé durant ce tour, augmenter le compteur global
        if not progress_this_turn:
            no_progress_global += 1
            print("Aucun progrès réalisé pendant ce tour.")
        else:
            no_progress_global = 0
        
        # Si plusieurs tours consécutifs sans progrès, arrêter la simulation
        if no_progress_global >= 2:
            print("Aucun progrès pendant 2 tours consécutifs. Fin de la simulation.")
            return
        
        # Changer de joueur pour le tour suivant et afficher l'état du plateau
        current_player = "N" if current_player == "B" else "B"
        print("\n--- Nouveau tour, joueur {} ---".format(current_player))
        afficher_plateau(plateau)
    
    print("Nombre maximum de tours atteint. Fin de la simulation.")

if __name__ == "__main__":
    main_auto()