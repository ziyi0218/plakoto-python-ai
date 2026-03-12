#!/usr/bin/env python3
"""Text interface launcher for Plakoto game."""

import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from plakoto.interfaces.text_interface import TextInterface

def main():
    """Main function for text interface."""
    
    interface = TextInterface()
    
    
    try:
        interface.run()
    except KeyboardInterrupt:
        print("\n\nJeu interrompu par l'utilisateur.")
    except Exception as e:
        print(f"Erreur lors de l'exécution du jeu: {e}")

if __name__ == "__main__":
    main()
