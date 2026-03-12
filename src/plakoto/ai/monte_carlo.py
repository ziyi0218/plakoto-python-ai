import os
from ..core.board import *
from ..core.moves import *
from concurrent.futures import ProcessPoolExecutor, as_completed

# ------------------ SIMULATEUR ENTIEREMENT ALEATOIRE ------------------
def simulateur(
    plateau_init: Dict,
    joueur_init: str,
    max_turns: int = 120
) -> Optional[str]:
    """
    Version optimisée pour vitesse max : simulateur de partie random sans impression, sans vérifications lourdes.
    """
    
    board = copy_plateau(plateau_init)
    current = joueur_init

    turns = 0

    while turns < max_turns:
        turns += 1
        dice = lance_de()

        # Inline macro generation simple et rapide
        all_moves = []
        in_home = all_in_home(board, current)
        used = set()

        for i, d in enumerate(dice):
            origins = get_movable_pieces(board, current)
            random.shuffle(origins)
            for origine in origins:
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

# ------------------ GLOBAL PROCESS POOL ------------------

_global_executor = ProcessPoolExecutor(max_workers=os.cpu_count())

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

    
    futures = { _global_executor.submit(_worker_seq, arg): seq
                for arg, seq in zip(tasks, valid_seqs) }
    for fut in as_completed(futures):
        seq = futures[fut]
        wins = 0
        try:
            wins = fut.result()
        except Exception as e:
            print(f"Simulation for move {seq} failed: {e}")
        
        if wins > best_wins or (wins == best_wins and random.choice([True, False])):
            best_wins, best_seq = wins, seq
    return best_seq