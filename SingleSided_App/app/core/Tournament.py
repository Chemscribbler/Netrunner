import pandas as pd
import numpy as np
import networkx as nx
import random
try:
    from ..core.Player import Player
    from ..core.Bye_Player import Bye_Player
except ImportError:
    from Player import Player
    from Bye_Player import Bye_Player


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
        bye = Bye_Player(self)
        self.player_dict[bye.id] = bye        
        
    def make_score_penalty_array(self):
        df = np.array([[(player.score)/self.win_points for player in self.player_dict.values()]])
        df = abs(df - df.T)
        df = (df*(df+1))/2*self.score_factor
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

            p1_good = p1.check_allowed_pairing(p2.id, self.round)
            p2_good = p2.check_allowed_pairing(p1.id, self.round)

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

            if p1.is_bye or p2.is_bye:
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
            

    def drop_player(self, player):
        try:
            del self.player_dict[player.id]
            if self.round > 0:
                self.dropped_players[player.id] = player
                try:
                    del self.player_dict[-1]
                except KeyError:
                    self.add_bye_player()
                player.name = player.name + " (dropped)"
                return True
            else:
                player.name = player.name + " (dropped)"
                return True
        except (KeyError, AttributeError):
            print(f"{player} does not seem to be in the tournament")
            return False
    
    def get_lowest_score(self):
        min_score = 100
        for plr in self.player_dict.values():
            if not plr.is_bye:
                if plr.score < min_score:
                    min_score = plr.score
        return min_score
    

    def record_result(self, p1_id, p2_id, p1_points, p2_points):
        """
        Use to record/report a match result.
        p1_id: the numeric id of either player
        p2_id: the numeric id of the other player
        p1_points: Number of points p1 recieves (should be 3/1/0)
        p2_points: Number of points p1 recieves (should be 3/1/0)
        """
        p1 = self.player_dict[p1_id]
        p2 = self.player_dict[p2_id]
        rnd = self.round

        if p1.round_dict[rnd]["opp_id"] != p2_id:
            raise ValueError(f"Players ({p1.name}, {p2.name}) are not playing this round")
        try:
            p1.round_dict[rnd]['result']
            raise ValueError(f"Players ({p1.name}, {p2.name}) already have a recorded result, did you mean 'ammend_result'?")
        except KeyError:
            pass
        
        if p1_id == -1:
            p1_points = 0
            p2_points = self.win_points
        elif p2_id == -1:
            p1_points = self.win_points
            p2_points = 0

        p1.record_result(rnd, p1_points)
        p2.record_result(rnd, p2_points)
        return (p1_id, p1_points, p2_id, p2_points)
    
    def ammend_result(self, p1_id, p2_id, p1_points, p2_points):
        """
        Use to ammend a match result.
        p1_id: the numeric id of either player
        p2_id: the numeric id of the other player
        p1_points: Number of points p1 recieves (should be 3/1/0)
        p2_points: Number of points p1 recieves (should be 3/1/0)
        """
        p1 = self.player_dict[p1_id]
        p2 = self.player_dict[p2_id]
        rnd = self.round

        if p1.round_dict[rnd]["opp_id"] != p2_id:
            raise ValueError(f"Players ({p1.name}, {p2.name}) are not playing this round")
        
        if p1_id == -1:
            p1_points = 0
            p2_points = self.win_points
        elif p2_id == -1:
            p1_points = self.win_points
            p2_points = 0

        p1.ammend_result(rnd, p1_points)
        p2.ammend_result(rnd, p2_points)
        return (p1_id, p1_points, p2_id, p2_points)


    def check_round_done(self):
        """
        Utility function to test if all pairs in the given round have reported results
        If it returns 'True' the round is done
        Otherwise it will return false and print a message for each player
        """
        exceptions = 0
        for plr in self.player_dict.values():
            try:
                plr.round_dict[self.round]["result"]
            except KeyError:
                print(f"Player {plr.name} does not have a recorded result for this round {self.round}")
                exceptions += 1
                continue
        if exceptions > 0:
            return False
        else:
            return True

    def pair_round(self):
        """
        Pairs round automatically- should allow for people to rematch with opposite sides
        """
        if not self.check_round_done():
            raise ValueError("Not all pairs have reported")
        self.round += 1
        self.make_initial_graph()
        iteration = 1
        while not self.pairings_done:
            print(iteration)
            iteration += 1
            self.make_pairings()
            self.assign_sides()
            self.test_pairings()
        for pair in self.pairings:
            pdct = self.player_dict
            if pdct[pair[0]].is_bye:
                pdct[pair[1]].recieved_bye = True
            if pdct[pair[1]].is_bye:
                pdct[pair[0]].recieved_bye = True
    
    def finish_round(self,pair_next=True):
        """
        Checks that the round is done, and depending on optional arguments, starts next round
        pair_next: If True (default) will pair the next round, otherwise leave the round unpaired (can pair with pair_round)
        display_rankings: If true (default) will print current standings
        """
        if not self.check_round_done():
            raise ValueError("Not all pairs have reported")
        self.compute_sos()
        self.compute_ext_sos()
        if pair_next:
            self.pair_round()
    
    def compute_sos(self):
        for player in self.player_dict.values():
            opponent_total_score = 0
            opponents_games_played = 0
            for rnd in player.round_dict.values():
                try:
                    opponent = self.player_dict[rnd['opp_id']]
                    if opponent.is_bye:
                        continue
                except KeyError:
                    try:
                        opponent = self.dropped_players[rnd['opp_id']]
                        if opponent.is_bye:
                            continue
                    except:
                        continue
                opponent_total_score += opponent.score
                opponents_games_played += len(opponent.round_dict)
            if opponents_games_played == 0:
                #Handling div by 0 issues
                opponents_games_played = 1
            player.sos = opponent_total_score/opponents_games_played

    def compute_ext_sos(self):
        for player in self.player_dict.values():
            opponents_total_sos = 0
            opponents_games_played = 0
            for rnd in player.round_dict.values():
                try:
                    opponent = self.player_dict[rnd['opp_id']]
                    if opponent.is_bye:
                        continue
                except KeyError:
                    try:
                        opponent = self.dropped_players[rnd['opp_id']]
                        if opponent.is_bye:
                            continue
                    except:
                        continue
                opponents_total_sos += opponent.sos
                opponents_games_played += len(opponent.round_dict)
            if opponents_games_played == 0:
                #Handling div by 0 issues
                opponents_games_played = 1
            player.ext_sos = opponents_total_sos/opponents_games_played