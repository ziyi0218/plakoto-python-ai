import pygame
from sys import exit
import random
import sys
from typing import Dict, List, Tuple, Optional
import math

# ------------------------------ #
# 241227 mybestfriendisAzeryoma

# 24/05 initialisation

# 03/06 surfaces(plateau triangles) + rect_pions

# 04/06 fixer 24 chiffres + [def] afficher_pions

# 07/06 construire background + infos(surface) + [def] afficher_de

# 12/06 rect_cases + [def] click_lance、is_in_rect、get_indice_case + button "lance"

# 15/06 ajouter et modifier les fonctions de interface textuelle + construire main

# 20/06 ajouter deux etoiles (return indice de case `-1` et `24` )  pour sortir des pions

# 22/06 affichage_winner

# ------------------------------- #

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Plakoto')
clock = pygame.time.Clock()

background = pygame.Surface((1200, 600))
background.fill('grey17')
# colours

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# ------------------------- #
COLOR_01 = 'chocolate4'
COLOR_02 = 'khaki1'
COLOR_03 = 'firebrick'
COLOR_04 = 'forestgreen'
COLOR_05 = 'palegreen3'
COLOR_06 = 'palegreen4'
COLOR_07 = 'firebrick'
color_star = 'gold1'


# variables
'''plateau'''
plateau_x, plateau_y = 40, 40  # la position de plateau
H = 400
W = 600
r = W/30
h = H/16
sous_pla1_x, sous_pla1_y = plateau_x + 2*r, plateau_y + h
sous_pla2_x, sous_pla2_y = plateau_x + 16*r, plateau_y + h

'''table d'infos'''
infos_x, infos_y = 680, 40
infos_H = 12 * h
infos_W = 24 * r
sous_infos_x, sous_infos_y = infos_x, infos_y + infos_H / 3



# surfaces
'''plateau'''
plateau = pygame.Surface((W, H))
plateau.fill(COLOR_01)
sous_pla1 = pygame.Surface((12*r, 14*h))
sous_pla2 = pygame.Surface((12*r, 14*h))
sous_pla1.fill(COLOR_02)
sous_pla2.fill(COLOR_02)

'''infos'''
infos = pygame.Surface((infos_W, infos_H))
infos.fill(COLOR_05)
sous_infos = pygame.Surface((infos_W, infos_H/3))
sous_infos.fill(COLOR_06)



# pions & positions

color_pion_B = 'white'
color_pion_N = 'black'

# 1. rect_pions --- Type:dict de dict
rect_pions = {}
for i in range(24):
    if 0 <= i <= 5:    # sur I
        rect_pions[i] = {j: (sous_pla2_x + 12 * r - (i + 1) * 2 * r, sous_pla2_y + j * h, 2 * r, h) for j in range(6)}
    elif 6 <= i <= 11:   # sur II
        rect_pions[i] = {j: (sous_pla1_x + 12 * r - (i - 6 + 1) * 2 * r, sous_pla1_y + j * h, 2 * r, h) for j in range(6)}
    elif 12 <= i <= 17:   # sur III
        rect_pions[i] = {j: (sous_pla1_x + (i - 12) * 2 * r, sous_pla1_y + 14 * h - (j + 1) * h, 2 * r, h) for j in range(6)}
    else:    # sur IV
        rect_pions[i] = {j: (sous_pla2_x + (i - 18) * 2 * r, sous_pla2_y + 14 * h - (j + 1) * h, 2 * r, h) for j in range(6)}

# 2. rect_cases --- Type:dict
rect_cases = {}
for i in range(24):
    if 0 <= i <= 5:    # sur I
        rect_cases[i] = (sous_pla2_x + 12 * r - (i + 1) * 2 * r, sous_pla2_y, 2 * r, 6 * h)
    elif 6 <= i <= 11:   # sur II
        rect_cases[i] = (sous_pla1_x + 12 * r - (i - 6 + 1) * 2 * r, sous_pla1_y, 2 * r, 6 * h)
    elif 12 <= i <= 17:   # sur III
        rect_cases[i] = (sous_pla1_x + (i - 12) * 2 * r, sous_pla1_y + 8 * h, 2 * r, 6 * h)
    else:    # sur IV
        rect_cases[i] = (sous_pla2_x + (i - 18) * 2 * r, sous_pla2_y + 8 * h, 2 * r, 6 * h)


# fonctions (interface graphique) -------------------#################################################
def afficher_pions(plateau) -> None:
    # 24 cases de pions
    for i in range(24):
        count = len(plateau[i]) if isinstance(plateau[i], list) else 0
        if 1<= count <= 6:
            for j in range(count):
                if plateau[i][j] == 'B':
                    pygame.draw.ellipse(screen, color_pion_B, rect_pions[i][j])
                else:  # plateau[i][j] == 'N'
                    pygame.draw.ellipse(screen, color_pion_N, rect_pions[i][j])
        elif count > 6:
            for j in range(6):
                if plateau[i][j] == 'B':
                    pygame.draw.ellipse(screen, color_pion_B, rect_pions[i][j])
                else:  # plateau[i][j] == 'N'
                    pygame.draw.ellipse(screen, color_pion_N, rect_pions[i][j])

    # nombre de pions sortie
    nb_B = font_infos.render(str(plateau["off_B"]), False, COLOR_07)
    nb_N = font_infos.render(str(plateau["off_N"]), False, COLOR_07)
    rect_nb_B = nb_B.get_rect(midbottom=(infos_x + 10 * r, infos_y + 6 * h))
    rect_nb_N = nb_N.get_rect(midbottom=(infos_x + 10 * r, infos_y + 8 * h))
    screen.blit(nb_B, rect_nb_B)
    screen.blit(nb_N, rect_nb_N)

def afficher_de(dice) -> None:
    '''list --> None'''
    s = ""
    if dice:
        for d in dice:
            s = s + "  " + str(d)
        txt = font_infos.render(s, False, COLOR_07)
        txt_rt = txt.get_rect(midbottom=(infos_x + 16 * r, infos_y + 4 * h))
        screen.blit(txt,txt_rt)
    else:
        txt = font_infos.render("Click 'lance' !", False, COLOR_07)
        txt_rt = txt.get_rect(midbottom=(infos_x + 16 * r, infos_y + 4 * h))
        screen.blit(txt, txt_rt)

def click_lance(pos):
    '''tuple --> Bool
    pos: possition de mouse'''
    x, y = pos
    if (infos_x + 2 * r) <= x <= (infos_x + 6 * r) and (infos_y + h) <= y <= (infos_y + 3 * h):
        return True
    else:
        return False


def is_in_rect(pos, rect):
    '''tuple x tuple --> bool'''
    x, y = pos
    rect_x, rect_y, width, height = rect
    if rect_x <= x <= (rect_x + width) and rect_y <= y <= (rect_y + height):
        return True
    else:
        return False


def get_indice_case(pos):
    '''tuple --> Int
    pos : possition de mouse
    return indice de case (0-23)'''
    indice = None
    if is_in_rect(pos, rect_star1):
        return -1
    elif is_in_rect(pos, rect_star2):
        return 24
    else:
        for i in range(24):
            if is_in_rect(pos, rect_cases[i]):
                indice = i
        return indice




def afficher_message(message):
    '''Str --> None'''
    msg = font_lance.render(message, False, 'darkblue')
    msg_rect = msg.get_rect(midbottom=(infos_x + 12 * r, infos_y + 10.5 * h))
    screen.blit(msg, msg_rect)


def draw_star(surface, center, outer_radius, inner_radius, color):
    '''return rect!!'''
    x0, y0 = center
    points = []
    for i in range(10):
        angle_deg = i * 36
        angle_rad = math.radians(angle_deg)
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = x0 + math.cos(angle_rad - math.pi / 2) * radius
        y = y0 + math.sin(angle_rad - math.pi / 2) * radius
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

    # construire rect_star
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    return rect


# fonctions (interface textuelle) ----------------------##############################################
_macro_moves_cache = {}

def lance_de():
    """
    () -> List[int]
    Simule le lancer de deux dés et renvoie le résultat.
    """
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    if d1 == d2:
        return [d1] * 4
    else:
        return [d1, d2]


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
    if destination < -1 or destination > 24:
        return False

    if not plateau[origine]:
        afficher_message("Erreur : la case d'origine est vide.")
        return False

    if plateau[origine][-1] != joueur:
        afficher_message("Erreur : la pièce à la case d'origine ne vous appartient pas.")
        return False

    if (joueur == "B" and destination <= origine) or (joueur == "N" and destination >= origine):
        afficher_message("Erreur : mouvement dans le mauvais sens.")
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


def generate_macro_moves(board: Dict, dice: List[int], current_player: str) -> Dict[
    str, List[List[Tuple[int, int, int]]]]:
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
            rest_dice = remaining_dice[:i] + remaining_dice[i + 1:]
            for origine in get_movable_pieces(current_board, current_player):
                destination = origine + d if current_player == "B" else origine - d
                if in_home and (
                        (current_player == "B" and destination > 23) or (current_player == "N" and destination < 0)):
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


def filter_max_pratique(macro_dict: Dict[str, List[List[Tuple[int, int, int]]]]) -> Dict[
    str, List[List[Tuple[int, int, int]]]]:
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


def is_move_prefix_in_macro_moves(board: Dict, dice: List[int], current_player: str,
                                  player_move: Tuple[int, int, int]) -> bool:
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
                # print("(Info : coup autorisé car légal mais pas optimal.)")
                return True
    origine, destination, dist = player_move
    # if dist not in dice:
    #     return False
    if destination == 24 or destination == -1:
        return bearing_off_possible(board, origine, dist, current_player)
    simulated = simulate_move(board, origine, destination, current_player)
    return simulated is not None


# ------------------ GESTION DES COMMANDES ------------------
def gestion_deplacement(origine: int,destination: int, plateau: Dict, joueur: str, dice: List[int]) -> Tuple[bool, bool, List[int], str]:
    """
    (str, Dict, str, List[int]) -> Tuple[bool, bool, List[int]], str
    Gère l'exécution de la commande de l'utilisateur.
    """
    msg = ""
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
        msg = "Erreur : Aucun dé ne correspond à ce mouvement."
        return True, False, dice, msg
    player_move = (origine, destination, move_distance)
    if not is_move_prefix_in_macro_moves(plateau, dice, joueur, player_move):
        msg = "Erreur : ce micro coup n'est pas valide."
        return True, False, dice, msg
    if deplacer_pion(plateau, origine, destination, joueur):
        msg = f"Le joueur {joueur} a déplacé avec succès."
        try:
            dice.remove(move_distance)
        except ValueError:
            pass
        return True, True, dice, msg
    else:
        msg = "Déplacement échoué."
        return True, False, dice, msg



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




# ------------------ UTILITAIRES ------------------
def opponent(joueur: str) -> str:
    return "N" if joueur == "B" else "B"


def determiner_premier_joueur():
    """
    N et B lancent un dé chacun ; celui qui fait le plus grand score commence.
    En cas d'égalité, on relance.
    Retourne "N" ou "B".
    """
    while True:
        roll_N = random.randint(1, 6)
        roll_B = random.randint(1, 6)

        if roll_N > roll_B:
            msg = f"N : {roll_N}  B : {roll_B}--> N commence !"
            return "N", msg
        elif roll_B > roll_N:
            msg = f"N : {roll_N}  B : {roll_B}--> B commence !"
            return "B", msg






# background
'''
construire background (hors boucle) avec des elements fixes 
'''

'''plateau'''
background.blit(plateau, (plateau_x, plateau_y))
background.blit(sous_pla1, (sous_pla1_x, sous_pla1_y))
background.blit(sous_pla2, (sous_pla2_x, sous_pla2_y))


'''infos'''
background.blit(infos, (infos_x, infos_y))
background.blit(sous_infos, (sous_infos_x, sous_infos_y))

'''draw triangles on (I) '''
for i in range(6):
    if i % 2 == 0:
        color = COLOR_04
    else:
        color = COLOR_03

    triangle = [
        (sous_pla2_x + i * 2 * r, sous_pla2_y),
        (sous_pla2_x + (i + 1) * 2 * r, sous_pla2_y),
        (sous_pla2_x + r + i * 2 * r, sous_pla2_y + 6 * h)
    ]

    pygame.draw.polygon(background, color, triangle)

'''draw triangles on (II) '''
for i in range(6):
    if i % 2 == 0:
        color = COLOR_04
    else:
        color = COLOR_03

    triangle = [
        (sous_pla1_x + i * 2 * r, sous_pla1_y),
        (sous_pla1_x + (i + 1) * 2 * r, sous_pla1_y),
        (sous_pla1_x + r + i * 2 * r, sous_pla1_y + 6 * h)
    ]

    pygame.draw.polygon(background, color, triangle)

'''draw triangles on (III) '''
for i in range(6):
    if i % 2 == 0:
        color = COLOR_03
    else:
        color = COLOR_04

    triangle = [
        (sous_pla1_x + i * 2 * r, sous_pla1_y + 14 * h),
        (sous_pla1_x + (i + 1) * 2 * r, sous_pla1_y + 14 * h),
        (sous_pla1_x + r + i * 2 * r, sous_pla1_y + 8 * h)
    ]

    pygame.draw.polygon(background, color, triangle)

'''draw triangles on (IV) '''
for i in range(6):
    if i % 2 == 0:
        color = COLOR_03
    else:
        color = COLOR_04

    triangle = [
        (sous_pla2_x + i * 2 * r, sous_pla2_y + 14 * h),
        (sous_pla2_x + (i + 1) * 2 * r, sous_pla2_y + 14 * h),
        (sous_pla2_x + r + i * 2 * r, sous_pla2_y + 8 * h)
    ]

    pygame.draw.polygon(background, color, triangle)

'''fixer 24 chiffres'''
font_24 = pygame.font.Font(None, int(1.2 * h))
color_24 = 'khaki1'

# 1-6 (I)
for i in range(6):
    j = i + 1
    a = font_24.render(str(j), True, color_24)
    a_rect = a.get_rect(midbottom=(sous_pla2_x + 11 * r - i * 2 * r, sous_pla2_y))
    background.blit(a, a_rect)

# 7-12 (II)
for i in range(6):
    j = i + 7
    a = font_24.render(str(j), True, color_24)
    a_rect = a.get_rect(midbottom=(sous_pla1_x + 11 * r - i * 2 * r, sous_pla1_y))
    background.blit(a, a_rect)

# 13-18 (III)
for i in range(6):
    j = i + 13
    a = font_24.render(str(j), True, color_24)
    a_rect = a.get_rect(midbottom=(sous_pla1_x + r + i * 2 * r, sous_pla1_y + 15 * h))
    background.blit(a, a_rect)

# 19-24 (IV)
for i in range(6):
    j = i + 19
    a = font_24.render(str(j), True, color_24)
    a_rect = a.get_rect(midbottom=(sous_pla2_x + r + i * 2 * r, sous_pla2_y + 15 * h))
    background.blit(a, a_rect)



'''text fixe sur "infos" '''
font_infos = pygame.font.Font(None, int(1.8 * h))
color_infos_fixe = 'black'

text01 = font_infos.render("Résultat des dés", False, color_infos_fixe)
text01_rect = text01.get_rect(midbottom=(infos_x + 16 * r, infos_y + 2 * h))
background.blit(text01, text01_rect)

text02 = font_infos.render("off_B :", False, color_infos_fixe)
text02_rect = text02.get_rect(midbottom=(infos_x + 4 * r, infos_y + 6 * h))
background.blit(text02, text02_rect)

text03 = font_infos.render("off_N :", False, color_infos_fixe)
text03_rect = text03.get_rect(midbottom=(infos_x + 4 * r, infos_y + 8 * h))
background.blit(text03, text03_rect)

'''button "lance" '''
font_lance = pygame.font.Font(None, int(1.5 * h))
rect_lance = (infos_x + 2 * r, infos_y + h, 4 * r, 2 * h)
pygame.draw.rect(background, COLOR_07, rect_lance)
text_lance = font_lance.render("lance", False, color_24)
text_lance_rect = text_lance.get_rect(midbottom=(infos_x + 4 * r, infos_y + 2.5 * h))
background.blit(text_lance, text_lance_rect)

'''draw deux stars'''
rect_star1 = draw_star(background, (plateau_x + W, plateau_y), 2 * r, r, color_star)
rect_star2 = draw_star(background, (plateau_x + W, plateau_y + H), 2 * r, r, color_star)


######################## main #################################
dice = []
ori_dest = []
plateau = init_plateau()
winner = []
current_player, msg = determiner_premier_joueur()

while True:
    screen.blit(background, (0, 0))

    afficher_de(dice)

    # affiche winner
    if winner:
        msg = f"Le joueur {winner[0]} a gagné !"

    # afficher message
    afficher_message(msg)

    # afficher pions
    afficher_pions(plateau)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()

            # lancer de
            if dice == [] and click_lance(pos_mouse):
                dice = lance_de()

            # deplacement pion
            clicked_case = get_indice_case(pos_mouse)
            if clicked_case is not None:
                ori_dest.append(clicked_case)

            if len(ori_dest) == 2:
                origine, destination = ori_dest
                ori_dest = []

                continuer, move_executed, dice, msg = gestion_deplacement(origine, destination, plateau, current_player, dice)

                if check_victoire(plateau, current_player):
                    winner.append(current_player)

                if not continuer:
                    break


                if move_executed:
                    if check_victoire(plateau, current_player):
                        winner.append(current_player)
                    if dice:
                        if not peut_jouer_au_moins_un_de(plateau, dice, current_player):
                            msg = f"Aucun coup restant possible pour le joueur {current_player}. Le tour est passé."
                            dice = []
                            current_player = "N" if current_player == "B" else "B"
                            msg = f"C'est le tour du joueur {current_player}."
                        else:
                            msg = f"C'est le tour du joueur {current_player}."
                    else:
                        current_player = "N" if current_player == "B" else "B"
                        msg = f"C'est le tour du joueur {current_player}."



    # ------------------------------------------------------------ #
    # '''draw pions'''
    # pygame.draw.ellipse(screen, color_pion_B, rect_pions[14][1])
    # pygame.draw.ellipse(screen, color_pion_N, rect_pions[16][0])
    #
    # # test afficher_pions()
    # test_plateau = {i: [] for i in range(24)}
    # test_plateau[0] = ['N', 'B', 'B']
    # test_plateau[1] = list(7 * 'N')
    # test_plateau["off_B"] = 7
    # test_plateau["off_N"] = 0
    # afficher_pions(test_plateau)


    # ----------------------------------------------------------- #


    pygame.display.update()
    clock.tick(60)