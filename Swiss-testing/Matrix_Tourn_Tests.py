import unittest
from Matrix_Tourn import Tourney
from Player import Player
import random
import TestUtilities


class TestTournamentMethods(unittest.TestCase):

    def test_add_player(self):
        t = Tourney()
        new_player = Player()
        t.add_player(new_player)

        self.assertCountEqual(t.player_dict, {new_player.id: new_player})
    
    def test_add_duplicate_player(self):
        t = Tourney()
        new_player = Player()
        t.add_player(new_player)

        with self.assertRaises(ValueError):
            t.add_player(new_player)

    def test_add_player_late(self):
        t = Tourney()
        t.round = 1
        
        with self.assertRaises(ValueError):
            t.add_player(Player())


if __name__ == '__main__':
    unittest.main()