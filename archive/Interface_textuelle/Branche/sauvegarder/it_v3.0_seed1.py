import random
import copy
from datetime import datetime
import builtins
import sys
from typing import Dict, List, Tuple, Optional

random.seed(1)

#######################################################################################
# 21 mars rzy (v0-->v1)
# I.simplifier la partie de plateau. i.e. 4 fonctions---> 2 fonctions
# II. Le débogage (bug001) :

# 24 mars rzy (v1-->v2.0)
#   1.Ajouter "bear off" (sortir les pions)
#   2.Ajouter Max Pratique pour filtrer les macros coups

# 27 mars rzy (v2.0-->v2.2)    Le débogage (Bug002)
# La fonction modifiée:
#    - afficher_plateau(plateau)
# Bug002: Blocage d’un pion seul —— erreur d’affichage de pion dans le plateau (B—>N)

# 27 mars Ruby Ghanime (v2.2-->v2.3)
# Modifications:
# Problème d'affichage du tableau lorsqu'une case possède plus que 6 pions (exemple : "| +1 |" au lieu de "|+1|")
# Le programme ne s'arrete pas. Ajout de sys.exit() si un joueur a gagné

# 29 mars Hassrol  --> Le débogage (Bug004) (v2.3-->v2.4)
# Ajouter "input enter"
# La fonction modifiée:
#    - main

# 29 mars rzy   --> Le débogage (Bug003) (v2.4-->v2.5)
# Bug_003 : Impossible de sortir un pion du plateau

# 30 mars Hassrol --> Débogage (Bug004,Bug005) (v2.5)
# Bug_004 : Lorsqu'aucun coup est possible avec les dées, le jeu ne faisait pas passé le tour
# Bug_005 : Un dée était jouable mais il passait le tour
# Ajout de la fonction peut_jouer_au_moins_un_de()
# Ajustement du lancé de dée sur le main
# Modification sur is_move_prefix_in_macro_moves()

# 31 mars Ruby Ghanime (v2.5 ---> v2.6)
# Optimisation de la fonction generate_macro_moves(), moins de vérifications de conditions + dictionnaire plus rapide à générer
# Optimisation de la fonction gestion_commande(), moins de calculs de variables inutiles.
# Amélioration de la fonction existe_pion_plus_loin()
# Optimisation de la fonction filtrer_max_pratique(), la fonction supprime les doublons.

# Problème dans la fonction is_move_prefix_in_macro_moves(), la valeur du dé dans le tuple qui définit un coup était égal à celle dans la liste dé,
# alors qu'il aurait fallu avoir 24 - 

# 1 avril Hassrol --> Débogage (Ancien bug revenu, Bug_007, Patch sur les mouvements v2.6->v2.7)
# Back-up de la fonction generate_macro_moves(),is_move_prefix_in_macro_moves() et réajustement dans le main 
# Modification de la validation des coups : v2.6 = façon très stricte (max pratique) ------> Souple (valide, optimal ou simulé)
# Modification de move : v2.6 = Calcule abs(dest - orig) ------> Cherche une valeur dans les dés restants
# Bearing off avec dé trop grand : v2.6 = Refusé ------> Accepté si pion le plus éloigné
# Modification existe_pion_plus_lointain() : v2.6 = Regarde hors home board ------> Corrigée pour home board uniquement

# 5 avril rzy (v2)
# Redéfinition de la fonction "check_victoire"

# 7 avril Ruby (v3)
# Redéfinition des fonctions "generate_macro_moves" et "filter_macro_moves"

# 8 avril hassrol (v2.7)
# Compilation du travail de chacun

# 10 avril Mahdi 
# correction de la condition dans "generate_macro_moves" pour la vérification de la home board

# 16 avril hassrol (v2.8)
# Ajouter ai vs ai, benchmarks, etc. (Un système de test complet) 

# 17 avril rzy (v2.9)
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
'''
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

# ------------------ Cache global pour generate_macro_moves ------------------
_macro_moves_cache = {}

# ------------------ COPIE LÉGÈRE DU PLATEAU ------------------
def copy_plateau(board: Dict) -> Dict:
    """
    (Dict) -> Dict
    Réalise une copie du plateau. Les listes pour les cases numériques sont copiées.
    """
    new_board = {i: board[i][:] for i in range(24)}
    new_board["off_B"] = board["off_B"]
    new_board["off_N"] = board["off_N"]
    return new_board

# ------------------ CREATION DU PLATEAU ------------------
def init_plateau() -> Dict:
    """
    () -> Dict
    Initialise le plateau et place les pions de départ.
    """
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)
    plateau[23] = list("N" * 15)
    plateau["off_B"] = 0
    plateau["off_N"] = 0
    return plateau

# ------------------ AFFICHAGE DU PLATEAU ------------------
def afficher_plateau(plateau: Dict) -> None:
    """
    (Dict) -> None
    Affiche le plateau de jeu en mode ASCII.
    """
    print("\n" + "=" * 49)
    print(" " * 17 + "PLATEAU PLAKOTO")
    print("=" * 49 + "\n")
    print(f"(Sortis) B: {plateau['off_B']} | N: {plateau['off_N']}\n")
    cells = []
    for i in range(24):
        count = len(plateau[i]) if isinstance(plateau[i], list) else 0
        symbol = plateau[i][-1] if plateau[i] else ' '
        cells.append((count, symbol))
    haut = cells[:12]
    bas = cells[12:]
    for i in range(6, 0, -1):
        ligne = "|"
        for count, symbol in reversed(haut):
            if i == 6 and count > 5:
                ligne += f"+{count - 5}{symbol}|"
            elif count > i:
                ligne += f" {symbol} |"
            else:
                ligne += "   |"
        print(ligne)
    print("| " + " | ".join(
          plateau[i][0] if plateau[i] else " "
          for i in range(11, -1, -1)
         ) + " |")
    print("|" + " |".join(f"{i:2}" for i in range(12, 0, -1)) + " |")
    print("|" + "---|" * 12)
    print("|" + " |".join(f"{i:2}" for i in range(13, 25)) + " |")
    print("| " + " | ".join(
          plateau[i][0] if plateau[i] else " "
          for i in range(12, 24)
         ) + " |")
    for i in range(1, 7):
        ligne = "|"
        for count, symbol in bas:
            if i == 6 and count > 5:
                ligne += f"+{count - 5}{symbol}|"
            elif count > i:
                ligne += f" {symbol} |"
            else:
                ligne += "   |"
        print(ligne)

# ------------------ LANCEMENT DES DÉS ------------------
def lance_de() -> List[int]:
    """
    () -> List[int]
    Simule le lancer de deux dés et renvoie le résultat.
    """
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    if d1 == d2:
        return [d1] * 4
    else:
        return [d1, d2]

# ------------------ COMMANDES DU JEU ------------------
def afficher_commandes() -> None:
    """
    () -> None
    Affiche la liste des commandes disponibles pour le jeu.
    """
    print("\nCommandes disponibles :")
    print("  help                      -> Afficher la liste des commandes")
    print("  lance                     -> Lancer les dés")
    print("  plateau                   -> Afficher le plateau")
    print("  move <origine> <destination>  -> Déplacer un pion")
    print("  quit                      -> Quitter le jeu")

# ------------------ VERIFICATION DE DEPLACEMENT ------------------
def is_move_legal_by_dice(origine: int, destination: int, dice: List[int], joueur: str) -> bool:
    """
    (int, int, List[int], str) -> bool
    Vérifie si la distance du mouvement correspond à une valeur présente dans les dés.
    """
    move_distance = abs(destination - origine)
    if move_distance in dice:
        if joueur == "B" and destination > origine:
            return True
        if joueur == "N" and origine > destination:
            return True
    return False

# ------------------ HOME BOARD & BEARING OFF ------------------
def in_home_board(pos: int, joueur: str) -> bool:
    """
    (int, str) -> bool
    Vérifie si la position 'pos' se trouve dans la home board du joueur.
    """
    if joueur == "B":
        return 18 <= pos <= 23
    return 0 <= pos <= 5

def all_in_home(plateau: Dict, joueur: str) -> bool:
    """
    (Dict, str) -> bool
    Vérifie si tous les pions du joueur sont dans sa home board.
    """
    for i in range(24):
        if plateau[i]:
            for pion in plateau[i]:
                if pion == joueur and not in_home_board(i, joueur):
                        return False
    return True

def bearing_off_possible(plateau: Dict, origine: int, dice_value: int, joueur: str) -> bool:
    """
    (Dict, int, int, str) -> bool
    Vérifie si le pion en 'origine' peut sortir avec la valeur du dé 'dice_value'.
    """
    if not all_in_home(plateau, joueur):
        return False
    if joueur == "B":
        distance = 24 - origine
    else:
        distance = origine - (-1)
    if dice_value == distance:
        return True
    elif dice_value > distance:
        return not existe_pion_plus_lointain(plateau, joueur, origine)
    else:
        return False

def existe_pion_plus_lointain(plateau: Dict, joueur: str, origine: int) -> bool:
    """
    (Dict, str, int) -> bool
    Vérifie s'il existe un pion plus éloigné dans la home board.
    """
    if joueur == 'B':
        for i in range(origine - 1, 17, -1):
            if in_home_board(i, joueur) and plateau[i] and joueur in plateau[i]:
                return True
    else:
        for i in range(origine + 1, 6):
            if in_home_board(i, joueur) and plateau[i] and joueur in plateau[i]:
                return True
    return False

def bearing_off(plateau: Dict, origine: int, joueur: str) -> None:
    """
    (Dict, int, str) -> None
    Exécute l'action de bearing off en retirant le pion de la case 'origine'.
    """
    plateau[origine].pop()
    if joueur == "B":
        plateau["off_B"] += 1
    else:
        plateau["off_N"] += 1

# ------------------ DEPLACEMENT DE PION ------------------
def deplacer_pion(plateau: Dict, origine: int, destination: int, joueur: str) -> bool:
    """
    (Dict, int, int, str) -> bool
    Déplace un pion du plateau si le mouvement est valide.
    """

    if not plateau[origine]:
        print("Erreur : la case d'origine est vide.")
        return False
    
    if plateau[origine][-1] != joueur:
        print("Erreur : la pièce à la case d'origine ne vous appartient pas.")
        return False
    
    if (joueur == "B" and destination <= origine) or (joueur == "N" and destination >= origine):
        print("Erreur : mouvement dans le mauvais sens.")
        return False

    if joueur == "B" and destination == 24:
        dist = 24 - origine
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
    
    if destination < 0 or destination > 23:
        return False
    
    if plateau[destination]:
        if plateau[destination][-1] != joueur:
            if len(plateau[destination]) > 1:
                return False
            
    piece = plateau[origine].pop()
    plateau[destination].append(piece)
    return True

# ------------------ CONDITION DE VICTOIRE ------------------
def check_victoire(plateau: Dict, joueur: str) -> bool:
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


# ------------------ GÉNÉRATION DES MACRO COUPS ------------------
def get_movable_pieces(board: Dict, joueur: str) -> List[int]:
    """
    (Dict, str) -> List[int]
    Retourne la liste des indices où le joueur peut déplacer une pièce.
    """
    return [i for i in range(24) if board[i] and board[i][-1] == joueur]

def simulate_move(board: Dict, origine: int, destination: int, joueur: str) -> Optional[Dict]:
    """
    (Dict, int, int, str) -> Optional[Dict]
    Simule un mouvement sans modifier le plateau original et renvoie le nouveau plateau.
    """
    new_board = copy_plateau(board)
    if deplacer_pion(new_board, origine, destination, joueur):
        return new_board
    return None

def board_signature(board: Dict) -> str:
    """
    (Dict) -> str
    Crée une signature textuelle du plateau pour le caching.
    """
    main_part = '|'.join(''.join(board[i]) for i in range(24))
    off_part = f"Boff={board['off_B']},Noff={board['off_N']}"
    return main_part + "|" + off_part

def generate_macro_moves(board: Dict, dice: List[int], current_player: str) -> Dict[str, List[List[Tuple[int, int, int]]]]:
    """
    Version optimisée (itérative + cache + copies limitées) de generate_macro_moves.
    """
    key = (board_signature(board), tuple(dice), current_player)
    if key in _macro_moves_cache:
        return _macro_moves_cache[key]

    if not dice:
        sig = board_signature(board)
        result = {sig: [[]]}
        _macro_moves_cache[key] = result
        return result

    stack = [(copy_plateau(board), [], dice)]
    seen = set()
    results = {}

    in_home = all_in_home(board, current_player)

    while stack:
        current_board, current_macro, remaining_dice = stack.pop()

        sig = board_signature(current_board)
        if (sig, tuple(remaining_dice)) in seen:
            continue
        seen.add((sig, tuple(remaining_dice)))

        if not remaining_dice:
            results.setdefault(sig, []).append(current_macro)
            continue

        used_moves = set()

        for i, d in enumerate(remaining_dice):
            rest_dice = remaining_dice[:i] + remaining_dice[i+1:]
            for origine in get_movable_pieces(current_board, current_player):
                destination = origine + d if current_player == "B" else origine - d
                if in_home and ((current_player == "B" and destination > 23) or (current_player == "N" and destination < 0)):
                    destination = 24 if current_player == "B" else -1

                move = (origine, destination, d)
                if move in used_moves:
                    continue
                used_moves.add(move)

                board_copy = copy_plateau(current_board)
                if deplacer_pion(board_copy, origine, destination, current_player):
                    stack.append((board_copy, current_macro + [move], rest_dice))

    _macro_moves_cache[key] = results
    return results

# ------------------ MAX PRATIQUE ------------------
def score_macro_move(macro_move: List[Tuple[int, int, int]]) -> int:
    """
    (List[Tuple[int, int, int]]) -> int
    Calcule le score d'un macro-coup en fonction des distances parcourues.
    """
    total = 0
    for o, dest, d in macro_move:
        if dest == 24:  # B sort
            total += (24 - o)
        elif dest == -1:  # N sort
            total += o + 1
        else:
            total += abs(dest - o)
    return total

def filter_max_pratique(macro_dict: Dict[str, List[List[Tuple[int, int, int]]]]) -> Dict[str, List[List[Tuple[int, int, int]]]]:
    """
    (Dict[str, List[List[Tuple[int, int, int]]]]) -> Dict[str, List[List[Tuple[int, int, int]]]]
    Filtre les macro-coups pour ne conserver que ceux qui ont le score maximal.
    """

    filtered_dict = {}
    max_score_global = 0
    for coups in macro_dict.values():
        for coup in coups:
            s = score_macro_move(coup)
            if s > max_score_global:
                max_score_global = s

    for sig, coups in macro_dict.items():
        best_coups = []
        for coup in coups:
            if score_macro_move(coup) == max_score_global:
                best_coups.append(coup)
        if best_coups:
            filtered_dict[sig] = best_coups
    return filtered_dict

def is_move_prefix_in_macro_moves(board: Dict, dice: List[int], current_player: str, player_move: Tuple[int, int, int]) -> bool:
    """
    (Dict, List[int], str, Tuple[int, int, int]) -> bool
    Vérifie si le micro-coup 'player_move' est présent dans les macro-coups générés.
    """
    macro_moves = generate_macro_moves(board, dice, current_player)
    filtered = filter_max_pratique(macro_moves)
    for moves_list in filtered.values():
        for move_seq in moves_list:
            if move_seq and move_seq[0] == player_move:
                return True
    for moves_list in macro_moves.values():
        for move_seq in moves_list:
            if move_seq and move_seq[0] == player_move:
                print("(Info : coup autorisé car légal mais pas optimal.)")
                return True
    origine, destination, dist = player_move
    if dist not in dice:
        return False
    if destination == 24 or destination == -1:
        return bearing_off_possible(board, origine, dist, current_player)
    simulated = simulate_move(board, origine, destination, current_player)
    return simulated is not None

# ------------------ GESTION DES COMMANDES ------------------
def gestion_commande(cmd: str, plateau: Dict, joueur: str, dice: List[int]) -> Tuple[bool, bool, List[int]]:
    """
    (str, Dict, str, List[int]) -> Tuple[bool, bool, List[int]]
    Gère l'exécution de la commande de l'utilisateur.
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
        if joueur == "B" and destination > 23 and all_in_home(plateau, "B"):
            destination = 24
        if joueur == "N" and destination < 0 and all_in_home(plateau, "N"):
            destination = -1
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
        if not is_move_prefix_in_macro_moves(plateau, dice, joueur, player_move):
            print("Erreur : ce micro coup n'est pas valide.")
            return True, False, dice
        if deplacer_pion(plateau, origine, destination, joueur):
            print(f"Le joueur {joueur} a déplacé avec succès.")
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

def peut_jouer_au_moins_un_de(plateau: Dict, dice: List[int], joueur: str) -> bool:
    """
    (Dict, List[int], str) -> bool
    Vérifie s'il existe au moins un mouvement légal avec les dés restants.
    """
    for d in dice:
        for origine in get_movable_pieces(plateau, joueur):
            dest = origine + d if joueur == "B" else origine - d
            if joueur == "B" and all_in_home(plateau, "B") and dest > 23:
                dest = 24
            elif joueur == "N" and all_in_home(plateau, "N") and dest < 0:
                dest = -1
            if simulate_move(plateau, origine, dest, joueur) is not None:
                return True
    return False

############################ MAIN DU JEU ############################################
def main():
    """
    Boucle principale du jeu en interface texte.

    Entrée:
      - Aucune (lecture de commandes via input())
    Sortie:
      - Aucune (le jeu se termine quand un joueur gagne ou tape 'quit')
    """
    plateau = init_plateau()
    afficher_plateau(plateau)
    afficher_commandes()
    current_player = "B"  # Les pions blancs (B) commencent
    dice = []  # Au début du tour, aucun dé n'a été lancé
    print(f"\nC'est le tour du joueur {current_player}.")

    while True:
        if not dice:
            print("Veuillez lancer les dés d'abord (tapez 'lance').")

        cmd = input("\nEntrez une commande :").strip().lower()

        continuer, move_executed, dice = gestion_commande(cmd, plateau, current_player, dice)

        if check_victoire(plateau, current_player):
            print(f"Le joueur {current_player} a gagné !")
            sys.exit()

        if not continuer:
            break

        # Si les dés viennent juste d'être lancés, vérifier s’il y a des coups possibles
        if cmd == "lance":
            if not peut_jouer_au_moins_un_de(plateau, dice, current_player):
                print(f"Aucun coup légal possible pour le joueur {current_player}. Le tour est passé.")
                dice = []
                current_player = "N" if current_player == "B" else "B"
                print(f"\nC'est le tour du joueur {current_player}.")
                afficher_plateau(plateau)
                continue

        if move_executed:
            if check_victoire(plateau, current_player):
                print(f"Le joueur {current_player} a gagné !")
                sys.exit()
            if dice:
                if not peut_jouer_au_moins_un_de(plateau, dice, current_player):
                    print(f"Aucun coup restant possible pour le joueur {current_player}. Le tour est passé.")
                    dice = []
                    current_player = "N" if current_player == "B" else "B"
                    print(f"\nC'est le tour du joueur {current_player}.")
                else:
                    print(f"Valeurs restantes des dés : {dice}")
            else:
                current_player = "N" if current_player == "B" else "B"
                print(f"\nC'est le tour du joueur {current_player}.")

        afficher_plateau(plateau)
        continue  # retour début boucle

if __name__ == "__main__":
    #print(filter_max_pratique(generate_macro_moves(init_plateau(), [6, 6, 6, 6], 'B')))
    main()