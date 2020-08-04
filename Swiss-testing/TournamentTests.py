import unittest
import Tournament
import Player


def simple_pairing_setup():
    t = Tournament.Tournament()
    for _ in range(2):
        low_player = Player.Player()
        high_player = Player.Player()
        high_player.score = 1
        t.add_player(low_player)
        t.add_player(high_player)
    return t

class TestTournamentMethods(unittest.TestCase):

    def test_add_player(self):
        t = Tournament.Tournament()
        new_player = Player.Player()
        t.add_player(new_player)

        self.assertCountEqual(t.player_list, [new_player])
    
    def test_add_duplicate_player(self):
        t = Tournament.Tournament()
        new_player = Player.Player()
        t.add_player(new_player)

        with self.assertRaises(ValueError):
            t.add_player(new_player)

    def test_add_player_late(self):
        t = Tournament.Tournament()
        t.round = 1
        
        with self.assertRaises(ValueError):
            t.add_player(Player.Player())

    def test_number_of_pairing_groups(self):
        t = simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups, [0,1])

    def test_player_allocation_pairing_groups(self):
        t = simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups[0],[player for player in t.player_list if player.score == 0])
        self.assertCountEqual(t._score_groups[1],[player for player in t.player_list if player.score == 1])


if __name__ == '__main__':
    unittest.main()