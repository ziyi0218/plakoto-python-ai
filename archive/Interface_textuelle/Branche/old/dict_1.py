import random
import copy


############################ CREATION DU PLATEAU ############################################
def init_plateau():
    """Initialiser le plateau et placer les pièces de départ."""
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)  # 15 pions blancs (B)
    plateau[23] = list("N" * 15)  # 15 pions noirs (N)
    return plateau


############################ AFFICHAGE DU PLATEAU ############################################
def afficher_plateau(plateau):
    """Afficher le plateau en ASCII."""
    for i in range(24):
        print(f"{i + 1} : {''.join(plateau[i]) if plateau[i] else '-'}")


############################ LANCEMENT DES DÉS ############################################
def lance_de():
    """
    Simuler le lancer de deux dés.
    Si c'est un double, renvoyer 4 fois la même valeur, sinon renvoyer les deux valeurs.
    """
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    if d1 == d2:
        return [d1] * 4  # Double : peut être joué 4 fois
    else:
        return [d1, d2]


############################ COMMANDE DE JEU ##############################################
def afficher_commandes():
    """Afficher la liste des commandes disponibles."""
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
      - Pour les pions blancs (B), la condition de victoire est que les 15 pions blancs se trouvent dans la case 24 (indice 23).
      - Pour les pions noirs (N), la condition de victoire est que les 15 pions noirs se trouvent dans la case 1 (indice 0).
    """
    if joueur == "B":
        if len(plateau[23]) == 15:
            return True
    elif joueur == "N":
        if len(plateau[0]) == 15:
            return True
    return False


############################ GESTION DES COMMANDES ##########################################
def gestion_commande(cmd, plateau, joueur, dice):
    """
    Traiter la commande entrée par l'utilisateur et retourner un tuple :
    (continuer le jeu, déplacement effectué, dés restants).
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
        if not is_move_legal_by_dice(origine, destination, dice, joueur):
            print("Erreur : ce déplacement ne correspond pas aux valeurs des dés ou à la direction requise.")
            return True, False, dice
        if deplacer_pion(plateau, origine, destination, joueur):
            print(f"Le joueur {joueur} a déplacé avec succès.")
            move_distance = abs(destination - origine)
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


############################## FONCTIONS POUR MICRO / MACRO COUPS #####################################

def get_movable_pieces(board, joueur):
    """
    Retourner la liste des indices où le joueur peut déplacer une pièce,
    c'est-à-dire les cases non vides dont la pièce du dessus appartient au joueur.
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
    """
    new_board = copy.deepcopy(board)
    if deplacer_pion(new_board, origine, destination, joueur):
        return new_board
    return None


def board_signature(board):
    """
    Générer une signature du plateau sous forme de chaîne de caractères,
    qui résume l'état final du plateau.
    """
    return '|'.join(''.join(board[i]) for i in range(24))


def generate_macro_moves(board, dice, current_player):
    """
    Génère tous les macro coups possibles pour le joueur courant à partir du plateau et des dés disponibles.
    Retourne un dictionnaire dont les clés sont les signatures (état final du plateau)
    et les valeurs sont des listes de macro coups (chaque macro coup est une liste de micro coups).
    Un micro coup est représenté par un tuple (origine, destination, valeur_du_dé).
    """
    # Si aucun dé n'est disponible, on retourne la signature actuelle du plateau avec un macro coup vide.
    if not dice:
        sig = board_signature(board)
        return {sig: [[]]}

    macro_moves = {}
    movable = get_movable_pieces(board, current_player)
    for origine in movable:
        for d in dice:
            # Déterminer la destination en fonction du joueur
            if current_player == "B":
                destination = origine + d
            else:  # current_player == "N"
                destination = origine - d
            # Vérifier que la destination est dans les limites du plateau
            if destination < 0 or destination > 23:
                continue
            # Vérifier la légalité du micro coup avec ce dé (en utilisant uniquement la valeur d)
            if not is_move_legal_by_dice(origine, destination, [d], current_player):
                continue
            # Simuler le déplacement sur une copie du plateau
            new_board = simulate_move(board, origine, destination, current_player)
            if new_board is None:
                continue
            new_dice = dice.copy()
            try:
                new_dice.remove(d)
            except ValueError:
                continue
            # Générer récursivement les macro coups pour le reste des dés
            subsequent_moves = generate_macro_moves(new_board, new_dice, current_player)
            for sig, moves_list in subsequent_moves.items():
                new_sig = sig  # Pour simplifier, on utilise directement la signature finale du plateau.
                for moves in moves_list:
                    full_move = [(origine, destination, d)] + moves
                    if new_sig not in macro_moves:
                        macro_moves[new_sig] = []
                    macro_moves[new_sig].append(full_move)
    return macro_moves


def test_generate_macro_moves():
    """
    Fonction de test pour générer et afficher les macro coups possibles.
    Par exemple, pour un tour où les dés obtenus sont [3, 4] et le joueur courant est "B".
    """
    board = init_plateau()
    # On suppose ici que le joueur "B" (blanc) doit avancer (de l'indice plus petit à l'indice plus grand)
    dice = [3, 4]
    current_player = "B"
    macro_moves_dict = generate_macro_moves(board, dice, current_player)
    print("Macro coups générés (signature -> liste de macro coups) :")
    for sig, moves_list in macro_moves_dict.items():
        print("Signature :", sig)
        for move_seq in moves_list:
            print("Macro coup :", move_seq)


############################ MAIN DU JEU ############################################
def main():
    """Boucle principale du jeu en interface texte, vérifiant la légalité des déplacements en interne sans afficher toutes les options légales."""
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
            # Vérifier la condition de victoire après un déplacement réussi
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
    # Pour tester la génération des macro coups, décommentez la ligne suivante :
    test_generate_macro_moves()

    # Pour lancer le jeu en mode texte, utilisez :
    #main()
