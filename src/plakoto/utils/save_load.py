"""Save and load functionality for Plakoto game."""

import pickle
import os
from typing import Dict, List, Tuple

DEFAULT_SAVE_FILE = "src/data/saves/savegame.pickle"

def sauvegarder_partie(plateau, current_player, dice, chemin_fichier=DEFAULT_SAVE_FILE):
    """
    Sauvegarde l'état actuel de la partie.
    
    Args:
        plateau: État du plateau
        current_player: Joueur actuel
        dice: Dés restants
        chemin_fichier: Chemin du fichier de sauvegarde
    """
    dossier = os.path.dirname(chemin_fichier)
    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)

    etat = {
        "plateau": plateau,
        "current_player": current_player,
        "dice": dice,
    }
    with open(chemin_fichier, "wb") as f:
        pickle.dump(etat, f)
    print(f"Partie sauvegardée dans {chemin_fichier} ✅")

def charger_partie(chemin_fichier=DEFAULT_SAVE_FILE):
    """
    Charge une partie sauvegardée.
    
    Args:
        chemin_fichier: Chemin du fichier de sauvegarde
        
    Returns:
        Tuple: (plateau, current_player, dice)
    """
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier non trouvé : {chemin_fichier}")

    with open(chemin_fichier, "rb") as f:
        etat = pickle.load(f)

    plateau = etat["plateau"]
    current_player = etat["current_player"]
    dice = etat["dice"]
    print(f"Partie chargée depuis {chemin_fichier} ✅")
    return plateau, current_player, dice
