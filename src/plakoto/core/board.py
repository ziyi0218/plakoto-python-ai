"""Board management for Plakoto game."""

import random
from typing import Dict, List, Tuple, Optional

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
    """
    if joueur == "B":
        if plateau[23] and plateau[23][0] == "N" and plateau[23][-1] != "N":
            return True 
        return plateau["off_B"] == 15
    else:  # joueur == "N"
        if plateau[0] and plateau[0][0] == "B" and plateau[0][-1] != "B":
            return True 
        return plateau["off_N"] == 15

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
