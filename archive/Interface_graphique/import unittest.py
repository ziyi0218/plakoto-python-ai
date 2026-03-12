import unittest
from typing import Dict
# Remplacez 'your_module' par le nom réel du module où se trouvent les fonctions
from your_module import all_in_home, in_home_board  

class TestAllInHome(unittest.TestCase):
    def test_toutes_pieces_dans_home(self):
        """Teste le cas où toutes les pièces du joueur sont dans sa zone de départ (home board)"""
        plateau = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
            6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
            12: [], 13: [], 14: [], 15: [], 16: [], 17: [],
            18: ['A'], 19: ['A'], 20: ['A'], 21: ['A'], 22: ['A'], 23: ['A']
        }
        self.assertTrue(all_in_home(plateau, 'A'))
    
    def test_une_piece_en_dehors_home(self):
        """Teste le cas où une pièce du joueur est en dehors de sa zone de départ"""
        plateau = {
            0: ['A'], 1: [], 2: [], 3: [], 4: [], 5: [],
            6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
            12: [], 13: [], 14: [], 15: [], 16: [], 17: [],
            18: ['A'], 19: ['A'], 20: ['A'], 21: ['A'], 22: ['A'], 23: ['A']
        }
        self.assertFalse(all_in_home(plateau, 'A'))
    
    def test_plateau_vide(self):
        """Teste le cas où le plateau est vide"""
        plateau = {i: [] for i in range(24)}
        self.assertTrue(all_in_home(plateau, 'A'))
    
    def test_pieces_adversaires_en_dehors(self):
        """Teste le cas où les pièces de l'adversaire sont en dehors, mais celles du joueur sont toutes dans sa zone de départ"""
        plateau = {
            0: ['B'], 1: [], 2: [], 3: [], 4: [], 5: [],
            6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
            12: [], 13: [], 14: [], 15: [], 16: [], 17: [],
            18: ['A'], 19: ['A'], 20: ['A'], 21: ['A'], 22: ['A'], 23: ['A']
        }
        self.assertTrue(all_in_home(plateau, 'A'))
    
    def test_plusieurs_pieces_en_dehors_home(self):
        """Teste le cas où plusieurs pièces du joueur sont en dehors de sa zone de départ"""
        plateau = {
            0: ['A'], 1: ['A'], 2: [], 3: [], 4: [], 5: [],
            6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
            12: [], 13: [], 14: [], 15: [], 16: [], 17: [],
            18: ['A'], 19: ['A'], 20: ['A'], 21: ['A'], 22: ['A'], 23: ['A']
        }
        self.assertFalse(all_in_home(plateau, 'A'))

if __name__ == '__main__':
    unittest.main()
