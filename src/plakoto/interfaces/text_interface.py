"""Text-based interface for Plakoto game."""

import sys
import pickle
from typing import Dict, List, Tuple, Optional
from ..core.board import *
from ..core.moves import *
from ..ai.monte_carlo import *
from ..utils.save_load import sauvegarder_partie, charger_partie

# Niveau de difficulté IA
NS_LEVEL = {
    'l': 30,
    'm': 500,
    'h': 1000
}

class TextInterface:
    """Text-based interface for Plakoto game."""
    
    
    def run(self):
        """Run the text interface with complete main function logic."""
        # ——— 1. Sélection du mode de jeu ———
        mode = ''
        while mode not in ('1', '2'):
            mode = input("Sélectionnez le mode : 1) Joueur vs Joueur    2) Joueur vs IA > ").strip()
        ia_activée = (mode == '2')

        if ia_activée:
            # Choix de la difficulté
            niveau = ''
            while niveau not in NS_LEVEL:
                niveau = input("Veuillez choisir la difficulté de l'IA [L]ow/[M]edium/[H]igh > ").strip().lower()
            ns = NS_LEVEL[niveau]
            joueur_humain = 'B'
            joueur_ia = 'N'
            print(f"\nMode IA : Vous = {joueur_humain}, IA = {joueur_ia}, simulations = {ns}\n")
        else:
            joueur_humain = joueur_ia = None  # non utilisé en mode PvP

        # ——— 2. Nouvelle partie ou chargement ———
        choix = input("N) Nouvelle partie  /  C) Charger une partie existante > ").strip().upper()
        if choix == "C":
            try:
                plateau, joueur_actuel, des = charger_partie()
            except (FileNotFoundError, pickle.PickleError):
                print("Aucun fichier valide, démarrage d'une nouvelle partie.")
                plateau = init_plateau()
                joueur_actuel = determiner_premier_joueur()
                des = []
        else:
            plateau = init_plateau()
            joueur_actuel = determiner_premier_joueur()
            des = []

        # ——— 3. Boucle de jeu principale ———
        afficher_plateau(plateau)
        afficher_commandes()
        print(f"C'est le tour du joueur {joueur_actuel}.\n")

        while True:
            # — Tour de l'IA ——
            if ia_activée and joueur_actuel == joueur_ia:
                print(f"\n=== Tour de l'IA ({joueur_ia}), simulations = {ns} ===")
                des = lance_de()
                print("Résultat des dés de l'IA :", des)

                # Génération des coups macros et sélection
                macro = generate_macro_moves(plateau, des, joueur_ia)
                candidats = [mv for seqs in macro.values() for mv in seqs]
                if candidats:
                    meilleure_seq = monte_carlo_select(plateau, joueur_ia, des, candidats, ns)
                    print("L'IA a choisi la séquence :", meilleure_seq)
                    # Exécution de la séquence choisie
                    for origine, destination, valeur in meilleure_seq:
                        from ..core.moves import deplacer_pion
                        deplacer_pion(plateau, origine, destination, joueur_ia)
                        des.remove(valeur)
                else:
                    print("Aucun coup possible, l'IA passe son tour.")
                    des = []

                afficher_plateau(plateau)
                if check_victoire(plateau, joueur_ia):
                    print("L'IA a gagné !")
                    break

                # Passage au joueur humain
                joueur_actuel = joueur_humain
                continue

            # — Tour du joueur humain ou joueur normal ——
            if not des:
                print("Veuillez lancer les dés d'abord (tapez 'lance').")

            cmd = input(f"\nEntrez une commande pour le joueur {joueur_actuel} : ").strip().lower()
            continuer, coup_exécuté, des = gestion_commande(cmd, plateau, joueur_actuel, des)

            if check_victoire(plateau, joueur_actuel):
                print(f"Le joueur {joueur_actuel} a gagné !")
                sys.exit()

            if not continuer:
                if input("Voulez-vous sauvegarder avant de quitter ? (O/N) > ").strip().upper() == "O":
                    sauvegarder_partie(plateau, joueur_actuel, des)
                print("Au revoir !")
                break

            # Si on vient de lancer les dés, vérifier les coups possibles
            if cmd == "lance":
                if not peut_jouer_au_moins_un_de(plateau, des, joueur_actuel):
                    print(f"Aucun coup légal possible pour le joueur {joueur_actuel}. Le tour est passé.")
                    des = []
                    joueur_actuel = "N" if joueur_actuel == "B" else "B"
                    print(f"\nC'est le tour du joueur {joueur_actuel}.")
                    afficher_plateau(plateau)
                    continue

            if coup_exécuté:
                if check_victoire(plateau, joueur_actuel):
                    print(f"Le joueur {joueur_actuel} a gagné !")
                    sys.exit()
                if des:
                    if not peut_jouer_au_moins_un_de(plateau, des, joueur_actuel):
                        print(f"Aucun coup restant possible pour le joueur {joueur_actuel}. Le tour est passé.")
                        des = []
                        joueur_actuel = "N" if joueur_actuel == "B" else "B"
                        print(f"\nC'est le tour du joueur {joueur_actuel}.")
                    else:
                        print(f"Valeurs restantes des dés : {des}")
                else:
                    joueur_actuel = "N" if joueur_actuel == "B" else "B"
                    print(f"\nC'est le tour du joueur {joueur_actuel}.")

            afficher_plateau(plateau)
            # Retour au début de la boucle
                
        print("Partie terminée !")
        