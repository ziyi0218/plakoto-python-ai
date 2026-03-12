import random
import sys
import time
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor


#random.seed(121)

#######################################################################################
# 1 avril hassrol
# Optimisation du programme

# 3 avril rzy (v1_auto players)
# Redéfinition de la fonction 

# 4 avril hassrol
# Ajustement pour monte-carlo

# 5 avril rzy (v2)
# Redéfinition de la fonction "check_victoire"

# 7 avril Ruby (v2.4)
# Redéfinition des fonctions "generate_macro_moves" et "filter_macro_moves"

# 8 avril hassrol (v2.7)
# Compilation du travail de chacun

# 10 avril Mahdi 
# correction de la condition dans "generate_macro_moves" pour la vérification de la home board

# 16 avril hassrol (v2.8)
# Ajouter ai vs ai, benchmarks, etc. (Un système de test complet) 

# 17 avril rzy (v2.9)
# Redéfinition de la fonction "check_victoire"

# 30 avril rzy (v3.0)
# Supprimer les parties inutile

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



# ------------------ SIMULATEUR ENTIEREMENT ALEATOIRE ------------------
def simulateur(
    plateau_init: Dict,
    joueur_init: str ,
    max_turns: int 
) -> Optional[str]:
    board = copy_plateau(plateau_init)
    current = joueur_init
    for _ in range(max_turns):
        dice = lance_de()
        while dice:
            macro = generate_macro_moves(board, dice, current)
            moves = [m for seq in macro.values() for m in seq]
            if not moves:
                break
            chosen = random.choice(moves)
            used = False
            for o, dest, d in chosen:
                if deplacer_pion(board, o, dest, current):
                    if d in dice:
                        dice.remove(d)
                        used = True
                        if check_victoire(board, current):
                            return current
                else:
                    break
            if not used:
                break
        current = opponent(current)
    return None

# ------------------ UTILITAIRES ------------------
def opponent(joueur: str) -> str:
    return "N" if joueur == "B" else "B"

# ------------------ APPLICATION D'UNE SEQUENCE DE MICRO COUPS ------------------
def simulate_macro_sequence(
    board: Dict,
    seq: List[Tuple[int, int, int]],
    joueur: str
) -> Optional[Dict]:
    board_copy = copy_plateau(board)
    for o, dest, d in seq:
        if not deplacer_pion(board_copy, o, dest, joueur):
            return None
    return board_copy

# ------------------ WORKER OPTIMISE ------------------
def _worker_seq(args):
    board_seq, joueur, dice_remain, ns, sim_max = args
    wins = 0
    for _ in range(ns):
        sim_board = copy_plateau(board_seq)
        sim_dice = dice_remain.copy()
        if simulateur(sim_board, opponent(joueur), max_turns=sim_max) == joueur:
            wins += 1
    return wins

# ------------------ MONTE CARLO PARALLEL OPTIMISE ------------------
def monte_carlo_select(
    board: Dict,
    joueur: str,
    dice: List[int],
    candidates: List[List[Tuple[int, int, int]]],
    ns: int,
    sim_max_turns: int = 120,
    n_procs: int = None
) -> List[Tuple[int, int, int]]:
    
   
     # ns==0 时直接随机挑一个宏走法
    if ns <= 0:
        return random.choice(candidates) if candidates else None
    
    best_seq, best_wins = None, -1
    tasks = []
    valid_seqs = []
    for seq in candidates:
        board_seq = simulate_macro_sequence(board, seq, joueur)
        if board_seq is None:
            continue
        dice_remain = dice.copy()
        for _, _, d in seq:
            if d in dice_remain:
                dice_remain.remove(d)
        tasks.append((board_seq, joueur, dice_remain, ns, sim_max_turns))
        valid_seqs.append(seq)
    if not tasks:
        return None
    with ProcessPoolExecutor(max_workers=n_procs) as exe:
        for seq, wins in zip(valid_seqs, exe.map(_worker_seq, tasks)):
            if wins > best_wins or (wins == best_wins and random.choice([True, False])):
                best_wins, best_seq = wins, seq
    return best_seq

# ------------------ AI vs AI ------------------
def match_ai_vs_ai(
    plateau_init: Dict,
    joueur_init: str,
    ns1: int,
    ns2: int,
    max_turns: int 
) -> Optional[str]:
    board = copy_plateau(plateau_init)
    current = joueur_init
    for _ in range(max_turns):
        dice = lance_de()
        macro = generate_macro_moves(board, dice, current)
        candidates = [mv for seqs in macro.values() for mv in seqs]
        if not candidates:
            current = opponent(current)
            continue
        ns = ns1 if current == joueur_init else ns2
        best_seq = monte_carlo_select(
            board, current, dice, candidates, ns, sim_max_turns=max_turns
        )
        if best_seq:
            for o, dest, d in best_seq:
                deplacer_pion(board, o, dest, current)
        if check_victoire(board, current):
            return current
        current = opponent(current)
    return None

# ------------------ BENCHMARK ------------------
if __name__ == "__main__":
    ns1 = 10  # 先手模拟次数
    ns2 = 30  # 后手模拟次数
    first_player = "B"  # 指定先手
    print(f"Simulation parameters: first_player={first_player}, ns_first={ns1}, ns_second={ns2}")
    results = {"B": 0, "N": 0, None: 0}
    for i in range(100):
        plateau = init_plateau()
        start = time.perf_counter()
        winner = match_ai_vs_ai(plateau, first_player, ns1, ns2, max_turns=120)
        elapsed = time.perf_counter() - start
        results[winner] += 1
        print(f"[Game {i+1:03d}] Winner = {winner!r}, time = {elapsed:.3f}s")
    print("\nSummary:")
    print(f"First player: {first_player}")
    print(f"ns1 (first): {ns1}, ns2 (second): {ns2}")
    print(f"  B wins : {results['B']}")
    print(f"  N wins : {results['N']}")
    print(f"  Draws  : {results[None]}")


