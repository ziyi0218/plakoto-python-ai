import random
import copy



random.seed(1)
############################## INPUT #####################################################
from datetime import datetime
import builtins

seed_value = 1

# 生成唯一的文件名
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
filename = f"Z_inputs_joueurs_{timestamp}_SEED_{seed_value}.txt"

# 打开日志文件以记录用户输入
log_file = open(filename, "w")

# 备份原始 input() 函数
original_input = builtins.input

# 定义自定义 input() 函数，自动记录用户输入
def custom_input(prompt=""):
    value = original_input(prompt)  # 获取用户输入
    log_file.write(value + "\n")  # 记录到日志文件
    log_file.flush()  # 立即写入，避免丢失数据
    return value  # 返回用户输入

# 替换内置 input() 为自定义函数
builtins.input = custom_input



############################ CREATION DU PLATEAU ############################################
def init_plateau():
    """
    Initialiser le plateau et placer les pièces de départ.

    Entrée:
      - Aucune
    Sortie:
      - dict[int, list[str]] : Un dictionnaire où chaque clé (0..23) correspond à une case
        et la valeur est une liste de pions ("B" ou "N").
    """
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)  # 15 pions blancs (B)
    plateau[23] = list("N" * 15)  # 15 pions noirs (N)
    return plateau


############################ AFFICHAGE DU PLATEAU ############################################
def afficher_plateau(plateau):
    """
    Afficher le plateau en ASCII.

    Entrée:
      - plateau: dict[int, list[str]]
    Sortie:
      - Aucune (affichage console)
    """
    for i in range(24):
        print(f"{i + 1} : {''.join(plateau[i]) if plateau[i] else '-'}")


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


############################ DEPLACEMENT DE PION ############################################
def deplacer_pion(plateau, origine, destination, joueur):
    """
    Déplacer une pièce selon les règles de base :
      - Vérifier que la case d'origine contient une pièce appartenant au joueur.
      - Si la case de destination contient déjà des pièces, vérifier si le déplacement est autorisé
        (si la case est occupée par plus d'une pièce adverse, le déplacement est interdit ;
         s'il y a une seule pièce adverse, afficher un message de blocage).

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
    if plateau[destination]:
        if plateau[destination][-1] != joueur:
            if len(plateau[destination]) > 1:
                print("Erreur : la case de destination est bloquée par l'adversaire.")
                return False
            elif len(plateau[destination]) == 1:
                print("Information : vous bloquez un pion adverse.")
    piece = plateau[origine].pop()
    plateau[destination].append(piece)
    return True


############################ CONDITION DE VICTOIRE #########################################
def check_victoire(plateau, joueur):
    """
    Vérifier si le joueur a gagné.
    Par exemple :
      - Pour les pions blancs (B), la condition de victoire est que les 15 pions blancs
        se trouvent dans la case 24 (indice 23).
      - Pour les pions noirs (N), la condition de victoire est que les 15 pions noirs
        se trouvent dans la case 1 (indice 0).

    Entrée:
      - plateau: dict[int, list[str]]
      - joueur: str ("B" ou "N")
    Sortie:
      - bool : True si le joueur a gagné, False sinon.
    """
    if joueur == "B":
        if len(plateau[23]) == 15 and plateau[23][-1] == "B":
            return True
    elif joueur == "N":
        if len(plateau[0]) == 15 and plateau[0][-1] == "N":
            return True
    return False


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

    Entrée:
      - board: dict[int, list[str]]
    Sortie:
      - str : Représentation textuelle du plateau (toutes les cases concaténées).
    """
    return '|'.join(''.join(board[i]) for i in range(24))


def generate_macro_moves(board, dice, current_player):
    """
    Génère tous les macro coups possibles pour le joueur courant à partir du plateau et des dés disponibles.
    Retourne un dictionnaire dont les clés sont les signatures (état final du plateau)
    et les valeurs sont des listes de macro coups (chaque macro coup est une liste de micro coups).
    Un micro coup est représenté par un tuple (origine, destination, valeur_du_dé).

    Entrée:
      - board: dict[int, list[str]]
      - dice: list[int]
      - current_player: str ("B" ou "N")
    Sortie:
      - dict[str, list[list[tuple[int,int,int]]]] :
        Un dictionnaire {signature: [liste_de_macro_coups]}, où signature est une chaîne représentant
        l'état final du plateau, et chaque macro coup est une liste de micro coups.
    """
    if not dice:
        sig = board_signature(board)
        return {sig: [[]]}

    macro_moves = {}
    movable = get_movable_pieces(board, current_player)
    for origine in movable:
        for d in dice:
            if current_player == "B":
                destination = origine + d
            else:  # current_player == "N"
                destination = origine - d
            if destination < 0 or destination > 23:
                continue
            if not is_move_legal_by_dice(origine, destination, [d], current_player):
                continue
            new_board = simulate_move(board, origine, destination, current_player)
            if new_board is None:
                continue
            new_dice = dice.copy()
            try:
                new_dice.remove(d)
            except ValueError:
                continue
            subsequent_moves = generate_macro_moves(new_board, new_dice, current_player)
            for sig, moves_list in subsequent_moves.items():
                new_sig = sig
                for moves in moves_list:
                    full_move = [(origine, destination, d)] + moves
                    if new_sig not in macro_moves:
                        macro_moves[new_sig] = []
                    macro_moves[new_sig].append(full_move)
    return macro_moves


def is_move_prefix_in_macro_moves(board, dice, current_player, player_move):
    """
    Vérifier si le micro coup du joueur (player_move), sous forme (origine, destination, valeur_dé),
    apparaît comme préfixe dans au moins un macro coup généré à partir du plateau actuel et des dés restants.

    Entrée:
      - board: dict[int, list[str]]
      - dice: list[int]
      - current_player: str ("B" ou "N")
      - player_move: tuple[int, int, int] (origine, destination, valeur_dé)
    Sortie:
      - bool : True si ce micro coup est un préfixe valide, False sinon.
    """
    macro_moves = generate_macro_moves(board, dice, current_player)
    for sig, moves_list in macro_moves.items():
        for move_seq in moves_list:
            if len(move_seq) >= 1 and move_seq[0] == player_move:
                return True
    return False


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
        if origine < 0 or origine > 23 or destination < 0 or destination > 23:
            print("Erreur : position hors limites. Veuillez entrer un nombre entre 1 et 24.")
            return True, False, dice
        move_distance = abs(destination - origine)
        player_move = (origine, destination, move_distance)
        # Vérifier si ce micro coup est un préfixe d'un macro coup valide
        if not is_move_prefix_in_macro_moves(plateau, dice, joueur, player_move):
            print("Erreur : ce micro coup n'est pas valide selon la génération des macro coups.")
            return True, False, dice
        # Effectuer le déplacement
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
        else:
            cmd = input("\nEntrez une commande :").strip().lower()

        continuer, move_executed, dice = gestion_commande(cmd, plateau, current_player, dice)
        if not continuer:
            break
        if move_executed:
            if check_victoire(plateau, current_player):
                print(f"Le joueur {current_player} a gagné !")
                break
            if dice:
                print(f"Valeurs restantes des dés : {dice}")
            else:
                current_player = "N" if current_player == "B" else "B"
                print(f"\nC'est le tour du joueur {current_player}.")
        afficher_plateau(plateau)


if __name__ == "__main__":
    main()