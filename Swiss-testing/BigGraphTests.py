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
        for _ in range(8):
            t.add_player(Player(score=2))
        for _ in range(8):
            t.add_player(Player())
        for _ in range(8):
            t.add_player(Player(score=1))
        t.find_pairings()
        for pair in t.pairings:
            self.assertEqual(pair[0].score, pair[1].score)
    
    def test_match_functions(self):
        t = Tournament()
        p1 = Player()
        p2 = Player()
        match = (p1, p2)
        t.sim_match(match)
        self.assertEqual(p1.opponent_list,[p2.id])

    def test_round_sim(self):
        t = Tournament()
        for _ in range(4):
            t.add_player(Player())
        t.sim_round()
        for player in t.player_list:
            self.assertEqual(len(player.opponent_list),1)



if __name__ == '__main__':
    unittest.main()