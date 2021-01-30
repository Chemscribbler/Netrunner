import Player
import Bye_Player
import pandas as pd
import numpy as np
import networkx as nx
import random

class Tournament(object):

    def __init__(self):
        self.player_dict = {}
        self.round = 0
        self.score_factor = 3
        self.pairing_graph = nx.Graph()
        self.pairings = []
        self.win_points = 3
        self.tie_points = 1
        self.pairings_done = False
        self.dropped_players = {}

    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        elif player.name in [plr.name for plr in self.player_dict.values()]:
            raise ValueError("Player of that name already registered")
        else:
            try:
                self.player_dict[player.id]
                raise ValueError("Player already in tournament")
            except KeyError:
                self.player_dict[player.id] = player

    def start_tourney(self):
        self.round = 1
        if len(self.player_dict) % 2 == 1:
            self.add_bye_player()
        #insert logic here for excluding people with round 1 byes
        starting_list = [x for x in self.player_dict.keys()]
        random.shuffle(starting_list)
        while len(starting_list) > 0:
            self.pairings.append((starting_list.pop(), starting_list.pop()))
        self.assign_sides()
        self.pairings_done = True

    def add_bye_player(self):
        bye = Bye_Player.Bye_Player()
        self.player_dict[bye.id] = bye        
        
    def make_score_penalty_array(self):
        df = np.array([[(player.score)/3 for player in self.player_dict.values()]])
        df = abs(df - df.T)*self.score_factor
        return df

    def make_side_penalty_array(self):
        df = np.array([[player.side_balance for player in self.player_dict.values()]])
        same_bias = ((df * df.T)> 0)
        np.fill_diagonal(same_bias,0)
        min_bias = np.minimum(abs(df), abs(df.T))
        return (8**(min_bias))*same_bias

    def make_initial_graph(self):
        self.pairings_done = False
        self.pairings = None
        pairing_matrix = 1000 - self.make_score_penalty_array() - self.make_side_penalty_array()
        pairing_matrix = pd.DataFrame(pairing_matrix,
            index=[key for key in self.player_dict.keys()],
            columns =[key for key in self.player_dict.keys()])
        self.pairing_graph = nx.convert_matrix.from_pandas_adjacency(pairing_matrix)

    def make_pairings(self):
        self.pairings = nx.max_weight_matching(self.pairing_graph,maxcardinality=True)

    def test_pairings(self):
        test_pass = True
        for pair in self.pairings:
            p1 = self.player_dict[pair[0]]
            p2 = self.player_dict[pair[1]]

            p1_good = p1.check_allowed_pairing(p2.id)
            p2_good = p2.check_allowed_pairing(p1.id)

            if p1_good and p2_good:
                pass
            else:
                self.pairing_graph[p1.id][p2.id]['weight']=0
                test_pass = False
        self.pairings_done = test_pass
        return test_pass
    
    def assign_sides(self):
        for pair in self.pairings:
            p1 = self.player_dict[pair[0]]
            p2 = self.player_dict[pair[1]]

            if p1.id == -1 or p2.id == -1:
                p1.record_pairing(p2.id, 0, self.round)
                p2.record_pairing(p1.id, 0, self.round)
                continue                
            
            elif p2.id in p1.get_opp_list():
                p1_side =  p1.flip_side(p2.id)
                p2_side =  p2.flip_side(p1.id)
            
            elif p1.side_balance == p2.side_balance:
                random_flip = random.randint(0,1)
                if random_flip == 0:
                    random_flip = -1
                p1_side = random_flip
                p2_side = random_flip * -1

            else:
                if p1.side_balance < p2.side_balance:
                    p1_side = 1
                    p2_side = -1
                else:
                    p1_side = -1
                    p2_side = 1
            
            p1.record_pairing(p2.id, p1_side, self.round)
            p2.record_pairing(p1.id, p2_side, self.round)
            

    def drop_player(self, player_name):
        for i, v in self.player_dict.items():
            if v.name == player_name:
                del self.player_dict[i]
                self.dropped_players[v.id] = v
                if len(self.player_dict) % 2 == 1:
                    try:
                        del self.player_dict[-1]
                    except KeyError:
                        self.add_bye_player()
                return True
        raise ValueError(f"{player_name} does not seem to be in the tournament")