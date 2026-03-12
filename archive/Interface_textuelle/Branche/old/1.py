import random


def init_plateau():
    """Initialise le plateau de jeu avec les pions de départ."""
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)  # 15 pions noirs
    plateau[23] = list("N" * 15)  # 15 pions blancs
    return plateau


def afficher_plateau(plateau):
    """Affiche le plateau de jeu."""
    for i in range(24):
        print(f"{i + 1} : {''.join(plateau[i]) if plateau[i] else '-'}")


def lance_de():
    """Simule le lancement de deux dés."""
    return random.randint(1, 6), random.randint(1, 6)


def afficher_commandes():
    """Affiche la liste des commandes disponibles."""
    print("\nCommandes disponibles :")
    print("  help   -> Affiche cette liste de commandes")
    print("  lance  -> Lance les dés")
    print("  plateau -> Affiche le plateau de jeu")
    print("  quit   -> Quitte le jeu")


def gestion_commande(cmd, plateau):
    """Gère les commandes utilisateur."""
    if cmd == "help":
        afficher_commandes()
    elif cmd == "lance":
        d1, d2 = lance_de()
        print(f"Résultat des dés : {d1}, {d2}")
    elif cmd == "plateau":
        afficher_plateau(plateau)
    elif cmd == "quit":
        print("Fin du jeu. À bientôt !")
        return False
    else:
        print("Commande inconnue. Tapez 'help' pour afficher les commandes disponibles.")
    return True


def main():
    """Boucle principale du jeu."""
    plateau = init_plateau()
    afficher_plateau(plateau)
    afficher_commandes()

    while True:
        cmd = input("\nEntrez une commande : ").strip().lower()
        if not gestion_commande(cmd, plateau):
            break


if __name__ == "__main__":
    main()
