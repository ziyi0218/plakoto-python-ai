import random
import copy
from datetime import datetime
import builtins

random.seed(1)

#######################################################################################
# 21 mars rzy
# I.simplifier la partie de plateau. i.e. 4 fonctions---> 2 fonctions


# II. Le débogage (bug001) :

# 1. Symptôme :
#    - Un déplacement valide s’exécutait correctement,
#      mais qu’une multitude de messages d’erreur s’affichaient, rendant la sortie confuse.

# 2. Cause identifiée :
#    - La fonction de vérification simule plusieurs déplacements pour générer les micro/macro-coups.
#    - Les coups non valides déclenchent l’affichage de messages d’erreur ou d’information inutiles.

# 3. Action corrective :
#    - J’ai supprimé les appels de type print qui généraient ces messages superflus,
#      pour ne conserver que ceux réellement pertinents pour le joueur.

# 4. Conclusion :
#    - Le code reste parfaitement fonctionnel et la logique de déplacement n’a pas été modifiée.
#    - La console n’est plus saturée de messages, offrant une expérience plus claire et fluide.


############################## INPUT ####################################################
'''Cette partie est utilisée pour générer automatiquement le fichier input'''

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

    for i in range(6, -1, -1):
        ligne = "|"
        for cell in reversed(haut):
            count, symbol = cell
            if i == 6 and count > 5:
                ligne += f" +{count - 5}{symbol} |"
            elif count > i:
                ligne += f" {symbol} |"
            else:
                ligne += "   |"
        print(ligne)

    print("|" + " |".join(f"{i:2}" for i in range(12, 0, -1)) + " |")
    print("|" + "---|" * 12)
    print("|" + " |".join(f"{i:2}" for i in range(13, 25)) + " |")

    for i in range(7):
        ligne = "|"
        for cell in bas:
            count, symbol = cell
            if i == 6 and count > 5:
                ligne += f" +{count - 5}{symbol} |"
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
    else:  # N
        return 0 <= pos <= 5

def all_in_home(plateau, joueur):
    """
    Vérifie si le joueur a tous ses pions dans sa home board,
    en tenant compte de la possibilité qu'ils soient sous un pion adverse.
    """
    for i in range(24):
        if plateau[i]:
            for pion in plateau[i]:
                if pion == joueur:
                    if not in_home_board(i, joueur):
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
        distance = 23 - origine
    else:  # joueur == "N"
        distance = origine - 0

    if dice_value == distance:
        return True
    elif dice_value > distance:
        # Vérifier s'il existe un pion plus éloigné
        if existe_pion_plus_lointain(plateau, joueur, origine):
            return False
        else:
            return True
    else:
        return False

def existe_pion_plus_lointain(plateau, joueur, origine):
    """
    Si joueur = B, on cherche s'il existe un pion sur un index > origine (dans home board).
    Si joueur = N, on cherche s'il existe un pion sur un index < origine (dans home board).
    """
    if joueur == "B":
        for i in range(origine+1, 24):
            if in_home_board(i, "B") and plateau[i] and plateau[i][-1] == "B":
                return True
    else:
        for i in range(0, origine):
            if in_home_board(i, "N") and plateau[i] and plateau[i][-1] == "N":
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
        dist = 23 - origine
        # On suppose qu'on a un dé >= dist
        # On doit vérifier bearing_off_possible
        # => Si OK, on sort le pion
        if bearing_off_possible(plateau, origine, dist, "B"):
            plateau[origine].pop()
            plateau["off_B"] += 1
            return True
        return False
    if joueur == "N" and destination == -1:
        dist = origine - 0
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
        return plateau["off_B"] == 15
    else:  # joueur == "N"
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
