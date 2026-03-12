from ..core.moves import *
from ..core.board import *

# ------------------------------ #
# LOGIQUE DE JEU
# ------------------------------ #

def opponent(joueur: str) -> str:
    return "N" if joueur == "B" else "B"


def determiner_premier_joueur():
    while True:
        roll_N = random.randint(1, 6)
        roll_B = random.randint(1, 6)

        if roll_N > roll_B:
            return "N", f"N : {roll_N}  B : {roll_B} --> N commence !"
        elif roll_B > roll_N:
            return "B", f"N : {roll_N}  B : {roll_B} --> B commence !"


def gestion_deplacement(origine: int, destination: int, plateau: Dict, joueur: str, dice: List[int]):
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
        return True, False, dice, "Erreur : Aucun dé ne correspond à ce mouvement."

    player_move = (origine, destination, move_distance)

    if not is_move_prefix_in_macro_moves(plateau, dice, joueur, player_move):
        return True, False, dice, "Erreur : ce micro coup n'est pas valide."

    if deplacer_pion(plateau, origine, destination, joueur):
        try:
            dice.remove(move_distance)
        except ValueError:
            pass
        return True, True, dice, f"Le joueur {joueur} a déplacé avec succès."

    return True, False, dice, "Déplacement échoué."


def update_turn_after_move(plateau, current_player, dice):
    if check_victoire(plateau, current_player):
        return current_player, dice, [current_player], f"Le joueur {current_player} a gagné !"

    if dice:
        if not peut_jouer_au_moins_un_de(plateau, dice, current_player):
            current_player = opponent(current_player)
            return current_player, [], [], f"Aucun coup restant possible. Tour au joueur {current_player}."
        return current_player, dice, [], f"C'est le tour du joueur {current_player}."

    current_player = opponent(current_player)
    return current_player, dice, [], f"C'est le tour du joueur {current_player}."
