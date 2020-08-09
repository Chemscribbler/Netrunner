import unittest
import Tournament
import Player
import random
import TestUtilities


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
        t = TestUtilities.simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups, [0,1])

    def test_player_allocation_pairing_groups(self):
        t = TestUtilities.simple_pairing_setup()
        t.find_pairing_groups()
        self.assertCountEqual(t._score_groups[0],[player for player in t.player_list if player.score == 0])
        self.assertCountEqual(t._score_groups[1],[player for player in t.player_list if player.score == 1])

    
    def test_pairing_flip(self):
        player_list = []
        for i in range(3):
            player_list.append(Player.Player())
            player_list[i].score = i
        t = Tournament.Tournament()
        for player in player_list:
            t.add_player(player)

        t.find_pairing_groups()
        t.choose_next_pairing_group()
        self.assertEqual(t._pairing_group_score, 2)
        self.assertTrue(t._pair_lowest_next)

        t.choose_next_pairing_group()
        self.assertEqual(t._pairing_group_score, 0)
        self.assertFalse(t._pair_lowest_next)

        t.choose_next_pairing_group()
        self.assertEqual(t._pairing_group_score, 1)
        self.assertTrue(t._pair_lowest_next)

    def test_factors(self):
        p1 = Player.Player()
        p2 = Player.Player()

        p1_index = 0
        p2_index = 1

        t = Tournament.Tournament()

        #Testing Old Floater
        self.assertEqual(t._compute_old_floater_penalty(p1, p2, p1_index, p2_index),0)
        p1.score = 1
        self.assertEqual(t._compute_old_floater_penalty(p1, p2, p1_index, p2_index), -475)
        
        #Testing side penalties
        self.assertEqual(t._compute_side_penalty(p1, p2), 0)
        p1.side_balance = 1
        p2.side_balance = -1
        self.assertEqual(t._compute_side_penalty(p1,p2), 0)
        p2.side_balance = 1
        self.assertEqual(t._compute_side_penalty(p1, p2), 25*8)
        p2.side_balance = 2
        self.assertEqual(t._compute_side_penalty(p1, p2),25*8)
        p1.side_balance = 2
        self.assertEqual(t._compute_side_penalty(p1,p2), 25*(8**2))
        p1.side_balance = -2
        self.assertEqual(t._compute_side_penalty(p1,p2),0)
        p2.side_balance = -2
        self.assertEqual(t._compute_side_penalty(p1,p2),25*(8**2))

        #Testing New Float Penalty
        self.assertEqual(t._compute_new_floater_penalty(p1_index, p2_index), 10)
        p2_index = 5
        self.assertEqual(t._compute_new_floater_penalty(p1_index,p2_index), 50)
        p1_index = 1
        self.assertEqual(t._compute_new_floater_penalty(p1_index,p2_index), 60)

    def test_node_addition(self):
        t = TestUtilities.simple_pairing_setup()
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.construct_network()
        for node in t._active_pairing_graph.nodes:
            self.assertIn(node.id, [player.id for player in t.player_list if player.score == 1])
        
    def test_sorting_function(self):
        p1 = Player.Player()
        p1.sos = 10
        p2 = Player.Player()
        p2.sos = 5
        p3 = Player.Player()
        p3.sos = 20
        p4 = Player.Player()
        p4.sos = 1

        t = Tournament.Tournament()
        t.add_player(p1)
        t.add_player(p2)
        t.add_player(p3)
        t.add_player(p4)

        t.find_pairing_groups()
        t.construct_network(iterate=False)
        self.assertEqual(list(t._active_pairing_graph.nodes), [p3, p1, p2, p4])
        self.assertNotEqual(list(t._active_pairing_graph.nodes), [p3, p1, p4, p2])

    def test_high_high_pairing(self):

        
        #Tests no valid pairings

        #tests even number- 1-2, 3-4, 5,-6, 7-8
        t = TestUtilities.eight_pairing_setup()
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.find_pairings(algorithm="high_high_swiss")
        PID_ordered_pairings = TestUtilities.reorder_by_PID(t)
        test_ordering = []
        for i in range(0,len(t.player_list),2):
            test_ordering.append((t.player_list[i],t.player_list[i+1]))
        self.assertCountEqual(PID_ordered_pairings, test_ordering)
        

        t = TestUtilities.four_by_two_setup()
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.find_pairings(algorithm="high_high_swiss")
        PID_ordered_pairings = TestUtilities.reorder_by_PID(t)
        test_ordering = []
        for i in range(0,len(t.player_list),2):
            test_ordering.append((t.player_list[i],t.player_list[i+1]))
        self.assertCountEqual(PID_ordered_pairings, test_ordering)

        #test even number with 1-2 already played- 1-3, 2-4 expected
        t =TestUtilities.eight_pairing_setup()
        t.player_list[0].opponent_list.append(t.player_list[1].id)
        t.player_list[1].opponent_list.append(t.player_list[0].id)
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.find_pairings(algorithm="high_high_swiss")
        PID_ordered_pairings = TestUtilities.reorder_by_PID(t)
        test_ordering = []
        test_ordering.append((t.player_list[0],t.player_list[2]))
        test_ordering.append((t.player_list[1],t.player_list[3]))
        for i in range(4,len(t.player_list),2):
            test_ordering.append((t.player_list[i],t.player_list[i+1]))
        self.assertCountEqual(PID_ordered_pairings, test_ordering)


        #test even number with 1-2, 3-4 already played (1-3, 2-4 expected)
        t =TestUtilities.eight_pairing_setup()
        t.player_list[0].opponent_list.append(t.player_list[1].id)
        t.player_list[1].opponent_list.append(t.player_list[0].id)
        t.player_list[3].opponent_list.append(t.player_list[4].id)
        t.player_list[4].opponent_list.append(t.player_list[3].id)
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.find_pairings(algorithm="high_high_swiss")
        PID_ordered_pairings = TestUtilities.reorder_by_PID(t)
        test_ordering = []
        test_ordering.append((t.player_list[0],t.player_list[2]))
        test_ordering.append((t.player_list[1],t.player_list[3]))
        for i in range(4,len(t.player_list),2):
            test_ordering.append((t.player_list[i],t.player_list[i+1]))
        self.assertCountEqual(PID_ordered_pairings, test_ordering)

        #tests odd number, drop down: 1-2, 3-4, 5-6, 7-8, 9
        t = TestUtilities.nine_pairing_setup()
        t.find_pairing_groups()
        t.choose_next_pairing_group()
        t.find_pairings(algorithm="high_high_swiss")
        # print(t.pairings)
        # [print(f"{player.id} {player.sos}") for player in t.player_list] 

        #tests odd number with dropped down: 1-9, 2-3, 4-5, 6-7, 8
        pass

if __name__ == '__main__':
    unittest.main()