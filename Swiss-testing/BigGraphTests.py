import unittest
from Tournament import Tournament
from Player import Player

class TestTournamentMethods(unittest.TestCase):

    def test_add_player(self):
        t = Tournament()
        new_player = Player()
        t.add_player(new_player)

        self.assertCountEqual(t.player_list, [new_player])
        self.assertGreater(new_player.str, 0)
    
    def test_add_duplicate_player(self):
        t = Tournament()
        new_player = Player()
        t.add_player(new_player)

        with self.assertRaises(ValueError):
            t.add_player(new_player)

    def test_add_player_late(self):
        t = Tournament()
        t.round = 1
        
        with self.assertRaises(ValueError):
            t.add_player(Player())

    def test_random_weighting_algo(self):
        t = Tournament()
        for _ in range(300):
            t.add_player(Player())
        for i in range(300):
            for j in range(300):
                if i >= j:
                    pass
                else:
                    self.assertGreaterEqual(t.random_Swiss_weights(i, j), 15000 - 100)
                    self.assertLessEqual(t.random_Swiss_weights(i,j), 15000)

    def test_second_round_pairing(self):
        t = Tournament()
        for _ in range(50):
            t.add_player(Player(score=2))
        for _ in range(50):
            t.add_player(Player())
        for _ in range(50):
            t.add_player(Player(score=1))
        t.find_pairings()
        for pair in t.pairings:
            self.assertEqual(pair[0].score, pair[1].score)


if __name__ == '__main__':
    unittest.main()