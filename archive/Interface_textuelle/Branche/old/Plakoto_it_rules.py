import random

plateau={i:[] for i in range(24)}

plateau[0]="B"*15
plateau[23]="N"*15


#afficher le plateau
def afficher_plateau(plateau):
    for i in range(24):
        print((i+1),":",plateau[i])


#lancer le dé
def lance_de():
    return random.randint(1, 6), random.randint(1, 6)

#Affiche la liste des commandes disponibles.
def afficher_commandes():
    print("\nCommandes disponibles :")
    print("  help   -> Affiche cette liste de commandes")
    print("  lance  -> Lance les dés")
    print("  plateau -> Affiche le plateau de jeu")
    print("  quit   -> Quitte le jeu")


def gestion_commande(cmd, plateau):
    if cmd == "help":
        afficher_commandes()
    elif cmd == "lance":
        d1, d2 = lance_de()
        print(f"Résultat des dés :",d1,d2)
    elif cmd == "plateau":
        afficher_plateau(plateau)
    elif cmd == "quit":
        print("Fin du jeu. À bientôt !")
        return False
    else:
        print("Commande inconnue. Tapez 'help' pour afficher les commandes disponibles.")
    return True





def main():
    afficher_plateau(plateau)
    afficher_commandes()

    while True:
        cmd = input("Entrez une commande : ")
        if not gestion_commande(cmd, plateau):
            break

main()
