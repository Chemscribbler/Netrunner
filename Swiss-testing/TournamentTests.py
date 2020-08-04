import unittest
import Tournament
import Player
import random


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

    def test_single_group(self):
        t = Tournament.Tournament()
        for _ in range(2):
            t.add_player(Player.Player())
        # t.add_player(Player.Player())

        t.find_pairing_groups()
        self.assertEqual(t._score_groups[0],t.player_list)

    def test_number_of_pairing_groups(self):
        t = simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups, [0,1])

    def test_player_allocation_pairing_groups(self):
        t = simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups[0],[player for player in t.player_list if player.score == 0])
        self.assertCountEqual(t._score_groups[1],[player for player in t.player_list if player.score == 1])

    def test_node_addition(self):
        t = simple_pairing_setup()
        t.find_pairing_groups()
        t.construct_network()
        for node in t._active_pairing_graph.nodes:
            self.assertIn(node.id, [player.id for player in t.player_list if player.score == 1])
    
    def test_pairing_flip(self):
        player_list = []
        for i in range(3):
            player_list.append(Player.Player())
            player_list[i].score = i
        t = Tournament.Tournament()
        for player in player_list:
            t.add_player(player)

        t.find_pairing_groups()
        self.assertEqual(t._next_unpaired_group, 2)
        self.assertTrue(t._pair_lowest_next)

        t.setup_next_network()
        self.assertEqual(t._next_unpaired_group, 0)
        self.assertFalse(t._pair_lowest_next)

        t.setup_next_network()
        self.assertEqual(t._next_unpaired_group, 1)
        self.assertTrue(t._pair_lowest_next)

    def test_random_weight_calculation(self):
        t = Tournament.Tournament()
        for _ in range(2):
            t.add_player(Player.Player())
        t.find_pairing_groups()
        for _ in range(100):
            t.construct_network(iterate=False)
            self.assertGreater(t._active_pairing_graph[t.player_list[0]][t.player_list[1]]['weight'], 10000 - 30)
            self.assertLess(t._active_pairing_graph[t.player_list[0]][t.player_list[1]]['weight'], 10000)


if __name__ == '__main__':
    unittest.main()