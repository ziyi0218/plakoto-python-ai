import random
import sys
import time
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

#random.seed(12)

#######################################################################################
# 1 avril hassrol
# Optimisation du programme

# 3 avril rzy (v1_auto players)
# Redéfinition de la fonction 

# 4 avril hassrol
# Ajustement pour monte-carlo

# 5 avril rzy (v2)
# Redéfinition de la fonction "check_victoire"

# 7 avril Ruby (v3)
# Redéfinition des fonctions "generate_macro_moves" et "filter_macro_moves"

# 8 avril hassrol
# Compilation du travail de chacun

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
    (Dict, str) -> bool
    Vérifie si le joueur a sorti tous ses pions.
    """
    if joueur == "B":
        return plateau["off_B"] == 15
    else:
        return plateau["off_N"] == 15

def check_blocage_victoire(plateau: Dict) -> None:
    """
    (Dict) -> None
    Vérifie si un blocage de pion conduit à une victoire et quitte le jeu.
    """
    if len(plateau[0]) >= 2 and plateau[0][-1] == "N" and plateau[0][-2] == "B":
        print("Le pion Blanc en 1 est bloqué par un pion Noir. Le joueur N a gagné !")
        afficher_plateau(plateau)
        sys.exit()
    if len(plateau[23]) >= 2 and plateau[23][-1] == "B" and plateau[23][-2] == "N":
        print("Le pion Noir en 24 est bloqué par un pion Blanc. Le joueur B a gagné !")
        afficher_plateau(plateau)
        sys.exit()

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

# ------------------ MAIN DU JEU ------------------
def main() -> None:
    """
    () -> None
    Fonction principale pour lancer le mode interactif du jeu.
    """
    plateau = init_plateau()
    afficher_plateau(plateau)
    afficher_commandes()
    current_player = "B"
    dice = []
    print(f"\nC'est le tour du joueur {current_player}.")
    while True:
        if not dice:
            print("Veuillez lancer les dés d'abord (tapez 'lance').")
        cmd = input("\nEntrez une commande :").strip().lower()
        continuer, move_executed, dice = gestion_commande(cmd, plateau, current_player, dice)
        if check_victoire(plateau, current_player):
            print(f"Le joueur {current_player} a gagné !")
            sys.exit()
        check_blocage_victoire(plateau)
        if not continuer:
            break
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
        continue

# ------------------ APPLICATION D'UNE SÉQUENCE DE MICRO COUPS ------------------
def simulate_macro_sequence(board: Dict, macro: List[Tuple[int, int, int]], current_player: str) -> Optional[Dict]:

    """
    (Dict, List[Tuple[int, int, int]], str) -> Optional[Dict]
    Applique la séquence de micro coups (macro coup) sur une copie du plateau.
    Retourne le nouveau plateau si la séquence est valide, sinon None.
    """

    board_copy = copy_plateau(board)

    for move in macro:
        origine, destination, _ = move
        if not deplacer_pion(board_copy, origine, destination, current_player):
            return None
    return board_copy

# ------------------ SIMULATION ALÉATOIRE D'UNE PARTIE ------------------
def simulate_random_game(board: Dict, starting_player: str) -> str:
    """
    Version optimisée pour vitesse max : simulateur de partie random sans impression, sans vérifications lourdes.
    """
    board = copy_plateau(board)
    current = starting_player
    turns = 0
    max_turns = 300

    while turns < max_turns:
        turns += 1
        dice = lance_de()

        # Inline macro generation simple et rapide
        all_moves = []
        in_home = all_in_home(board, current)
        used = set()

        for i, d in enumerate(dice):
            for origine in get_movable_pieces(board, current):
                destination = origine + d if current == "B" else origine - d
                if in_home:
                    if current == "B" and destination > 23:
                        destination = 24
                    if current == "N" and destination < 0:
                        destination = -1
                move = (origine, destination, d)
                if move in used:
                    continue
                used.add(move)
                if deplacer_pion(board, origine, destination, current):
                    all_moves.append(move)
                    break  # une seule tentative par dé

        if check_victoire(board, current):
            return current

        # Switch player
        current = "B" if current == "N" else "N"

    return current

def simulation_worker(args):
    board, macro, current_player = args
    board_copy = simulate_macro_sequence(board, macro, current_player)
    if board_copy is None:
        return 0
    winner = simulate_random_game(board_copy, "B" if current_player == "N" else "N")
    return 1 if winner == current_player else 0

# ------------------ ÉVALUATION MONTE CARLO DES MACRO COUPS ------------------

def monte_carlo_best_move(board: Dict, dice: List[int], current_player: str, num_simulations: int) -> Optional[List[Tuple[int, int, int]]]:
    """
    Version parallèle de Monte Carlo : chaque simulation est exécutée dans un processus séparé.
    """
    macro_moves = generate_macro_moves(board, dice, current_player)
    candidate_moves = []
    for moves in macro_moves.values():
        candidate_moves.extend(moves)

    if not candidate_moves:
        return None

    best_macro = None
    best_score = -1
    results = []

    with ThreadPoolExecutor() as executor:
        for macro in candidate_moves:
            tasks = [(board, macro, current_player)] * num_simulations
            scores = list(executor.map(simulation_worker, tasks))
            win_count = sum(scores)
            results.append(win_count)
            if win_count > best_score:
                best_score = win_count
                best_macro = macro

    return best_macro

# ------------------ SIMULATION MONTE CARLO (MODE 'sim') ------------------
def monte_carlo_simulation():
    """
    Version duel entre deux IA Monte Carlo avec paramètres différents pour chaque joueur.
    """
    plateau = init_plateau()
    current_player = "B"

    sim_params = {
        "B": 3,  # IA B utilise 100 simulations
        "N": 1    # IA N utilise 10 simulations
    }

    while True:
        print(f"\nTour du joueur {current_player}")
        dice = lance_de()
        print("Lancé de dés :", dice)

        num_sim = sim_params[current_player]
        best_macro = monte_carlo_best_move(plateau, dice, current_player, num_simulations=num_sim)

        if best_macro:
            print(f"IA {current_player} joue le macro coup (avec {num_sim} simulations) :", best_macro)
            for move in best_macro:
                origine, destination, _ = move
                deplacer_pion(plateau, origine, destination, current_player)
            check_blocage_victoire(plateau)
        else:
            print(f"Aucun coup possible pour le joueur {current_player} -> tour passé.")

        afficher_plateau(plateau)

        if check_victoire(plateau, current_player):
            print(f"Le joueur {current_player} a gagné la partie !")
            break

        current_player = "N" if current_player == "B" else "B"

# ------------------ BEST MOVE SANS MONTE CARLO ------------------

def fast_best_move(board: Dict, dice: List[int], current_player: str) -> Optional[List[Tuple[int, int, int]]]:
    macro_moves = generate_macro_moves(board, dice, current_player)
    candidate_moves = []
    for moves in macro_moves.values():
        candidate_moves.extend(moves)
    if not candidate_moves:
        return None
    return max(candidate_moves, key=score_macro_move)

# ------------------ PARTIE IA VS IA (MISE À JOUR) ------------------

def jouer_partie_ia_vs_ia(nb_sim_b: int, nb_sim_n: int, verbose=False, use_fast=False) -> str:
    plateau = init_plateau()
    current_player = "B"
    sim_params = {"B": nb_sim_b, "N": nb_sim_n}
    max_turns = 300
    turn_count = 0
    while turn_count < max_turns:
        dice = lance_de()
        num_sim = sim_params[current_player]

        if use_fast:
            best_macro = fast_best_move(plateau, dice, current_player)
        else:
            best_macro = monte_carlo_best_move(plateau, dice, current_player, num_simulations=num_sim)

        if verbose:
            print(f"Tour de {current_player} | Dés: {dice}")
            print(f"  > Coup choisi : {best_macro}")

        if best_macro:
            for move in best_macro:
                origine, destination, _ = move
                deplacer_pion(plateau, origine, destination, current_player)

        if check_victoire(plateau, current_player):
            return current_player
        
        current_player = "N" if current_player == "B" else "B"
        turn_count += 1

    print("Partie arrêtée après le nombre maximum de tours (match nul).")
    return "NUL"

# ------------------ BENCHMARK (MISE À JOUR) ------------------

def benchmark_ia_vs_ia(nb_parties: int, sim_b: int, sim_n: int, use_fast=False):
    start = time.time()
    victoires_b = 0
    victoires_n = 0

    print("Génération en cours...\n")
    for i in range(nb_parties):
        t0 = time.time()
        gagnant = jouer_partie_ia_vs_ia(sim_b, sim_n, use_fast=use_fast)
        t1 = time.time()
        print(f"Partie {i + 1}/{nb_parties} terminée en {t1 - t0:.2f}s - Gagnant : {gagnant}")
        if gagnant == "B":
            victoires_b += 1
        else:
            victoires_n += 1

    end = time.time()
    print("Résultat du benchmark :")
    print(f" - Victoires Blanc (B) [sim={sim_b}] : {victoires_b}")
    print(f" - Victoires Noir  (N) [sim={sim_n}] : {victoires_n}")
    print(f" - Temps total     : {end - start:.2f} secondes")

# ------------------ MAIN (MISE À JOUR) ------------------

if __name__ == "__main__":
    mode = input("Tapez 'jeu' pour le mode interactif ou 'sim' pour les simulations Monte Carlo ou 'benchmark' : ").strip().lower()
    if mode == "jeu":
        main()
    elif mode == "sim":
        monte_carlo_simulation()
    elif mode == "benchmark":
        fast = input("Mode rapide sans simulation ? (y/n) : ").strip().lower()
        use_fast = fast == "y"
        benchmark_ia_vs_ia(nb_parties=100, sim_b=3, sim_n=1, use_fast=use_fast)
    else:
        print("Mode inconnu. Veuillez redémarrer le programme et choisir 'jeu', 'sim' ou 'benchmark'.")
