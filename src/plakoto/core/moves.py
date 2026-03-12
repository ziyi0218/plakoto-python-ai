"""Move generation and validation for Plakoto game."""

import random
from typing import Dict, List, Tuple, Optional
from .board import copy_plateau, deplacer_pion, all_in_home, bearing_off_possible

# ------------------ Cache global pour generate_macro_moves ------------------
_macro_moves_cache = {}

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
    from .board import afficher_commandes, afficher_plateau
    from .moves import lance_de
    
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
    from .board import all_in_home
    from .moves import get_movable_pieces, simulate_move
    
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

# ------------------ UTILITAIRES ------------------
def opponent(joueur: str) -> str:
    """Get the opponent of the given player."""
    return "N" if joueur == "B" else "B"

def determiner_premier_joueur():
    """Determine the first player randomly."""
    return "B" if random.random() < 0.5 else "N"