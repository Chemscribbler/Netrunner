import Player
import pandas as pd
import numpy as np
import networkx as nx
from networkx import NetworkXError
from random import random, randint

class Tourney(object):

    def __init__(self):
        self.player_dict = {}
        self.round = 0
        self.score_factor = 3
        self.pairing_graph = nx.Graph()
        self.pairings = []

    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        else:
            try:
                self.player_dict[player.id]
                raise ValueError("Player already in tournament")
            except KeyError:
                self.player_dict[player.id] = player
    
    def make_score_penalty_array(self):
        df = np.array([[player.score for player in self.player_dict.values()]])
        df = abs(df - df.T)
        df = (df*(df+1))/2*self.score_factor
        return df
    
    def make_side_penalty_array(self):
        df = np.array([[player.side_balance for player in self.player_dict.values()]])
        same_bias = ((df * df.T)> 0)
        np.fill_diagonal(same_bias,0)
        min_bias = np.minimum(abs(df), abs(df.T))
        return (8**(min_bias))*same_bias
    
    def removed_played_edges(self):
        for player in self.player_dict.values():
            # print(f"{player.id}:{player.opponent_dict}")
            for opponent_id in player.opponent_dict.values():
                try:
                    # print(f"Removing {player.id} vs {opponent_id}")
                    self.pairing_graph[player.id][opponent_id]['weight']=0
                except:
                    pass
                # try:
                #     self.pairing_graph.remove_edge(player.id, opponent_id)
                # except NetworkXError:
                #     pass

    def construct_pairings_matrix(self):
        pairing_matrix = 1000-self.make_score_penalty_array() - self.make_side_penalty_array()
        pairing_matrix += np.random.random(size=(len(self.player_dict), len(self.player_dict)))
        pairing_matrix = pd.DataFrame(pairing_matrix,
            index=[key for key in self.player_dict.keys()],
            columns =[key for key in self.player_dict.keys()])
        return pairing_matrix

    def assign_sides(self):
        for pair in self.pairings:
            p1 = self.player_dict[pair[0]]
            p2 = self.player_dict[pair[1]]
            if p1.side_balance == p2.side_balance:
                random_flip = randint(0,1)
                if random_flip == 0:
                    random_flip = -1
                p1.side = random_flip
                p2.side = random_flip * -1

            else:
                if p1.side_balance < p2.side_balance:
                    p1.side = 1
                    p2.side = -1
                else:
                    p1.side = -1
                    p2.side = 1


    def make_pairings(self,allow_rematch=False,**kwargs):
        pairing_matrix = self.construct_pairings_matrix(**kwargs)  

        self.pairing_graph = nx.convert_matrix.from_pandas_adjacency(pairing_matrix)
        self.removed_played_edges()
        
        self.pairings = nx.max_weight_matching(self.pairing_graph,maxcardinality=True)

        self.assign_sides()
        

    def sim_match(self, pair):
        p1 = self.player_dict[pair[0]]
        p2 = self.player_dict[pair[1]]

        if p1.score != p2.score:
            p1.pairing_diff += abs(p1.score - p2.score)
            p2.pairing_diff += abs(p1.score - p2.score)
            p1.off_pair += 1
            p2.off_pair += 1
        
        win_percent = p1.str/(p1.str + p2.str)
        roll = random()
        
        if win_percent > roll:
            p1.record_match(p2.id, 1, self.round)
            p2.record_match(p1.id, 0, self.round)
        else:
            p1.record_match(p2.id,0,self.round)
            p2.record_match(p1.id,1,self.round)

    def sim_round(self,double_sided=False):
        self.round += 1
        self.make_pairings()
        if double_sided:
            self.round += 1
            for player in self.player_dict.values():
                player.side = 0
        sim_match = self.sim_match
        for pair in self.pairings:
            sim_match(pair)
            # self.sim_match(pair)
            if double_sided:   
                # self.sim_match(pair)             
                sim_match(pair)

        self.compute_sos()

    def sim_tourney(self,num_rounds, double_sided=False):
        while self.round < num_rounds:
            self.sim_round(double_sided)
        
    
    def compute_sos(self):
        for player in self.player_dict.values():
            opponent_total_score = 0
            opponents_games_played = 0
            for opponent_id in player.opponent_dict.values() :
                opponent = self.player_dict[opponent_id]
                opponent_total_score += opponent.score
                opponents_games_played += len(opponent.opponent_dict)
            player.sos = opponent_total_score/opponents_games_played
        