from Player import Player
import networkx as nx
import random

class Tournament():

    def __init__(self):
        self.player_list = []
        self._score_groups = {}
        self.round = 0
        self.pairings = set()
        self._active_pairing_graph = nx.Graph()
        self._unpaired_groups = []
        self._pairing_group_score = 0 #score integer
        self._pair_lowest_next = False
        self.round_paired = False
        self.LARGE_CONSTANT = 15000
        self.bye_player = Player(0)
        
    
    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        else:
            if player.id in [x.id for x in self.player_list]:
                raise ValueError("Player already in Tournament")
            else:
                self.player_list.append(player)
    
    #Constructs the graph of the active pairing group based on the model
    #algorithms: random_swiss, high_high_swiss, high_low_swiss, halfs_swiss, almafi_swiss 
    def construct_network(self,algorithm="random_swiss",iterate=False):
        new_graph = nx.Graph()

        #Sort by SoS then Score to deal with floaters
        self.player_list.sort(key= lambda player: player.sos, reverse=True)
        self.player_list.sort(key = lambda player: player.score, reverse=True)

        for player in self.player_list:
            new_graph.add_node(player)


        for i in range(len(self.player_list)):
            for j in range(len(self.player_list)):
                if i >= j:
                    pass
                else:
                    if self.player_list[i].id in self.player_list[j].opponent_list:
                        edge_weight = 0
                    else:
                        edge_weight = self.algorithms[algorithm](self, i, j)
                    new_graph.add_edge(self.player_list[i],self.player_list[j],weight = edge_weight)

        self._active_pairing_graph = new_graph


    def find_pairings(self, algorithm="random_swiss",**kwargs):
        self.construct_network(algorithm=algorithm,**kwargs)
        self.pairings = nx.max_weight_matching(self._active_pairing_graph)
        for pair in self.pairings:
            if pair[0].side_balance == pair[1].side_balance:
                random_flip = random.randint(0,1)
                if random_flip == 0:
                    random_flip = -1
                pair[0].side_balance += random_flip
                pair[0].side_order.append(random_flip)

                pair[1].side_balance += (random_flip*(-1))
                pair[1].side_order.append(random_flip*(-1))
            else:
                if pair[0].side_balance < pair[1].side_balance:
                    pair[0].side_balance += 1
                    pair[0].side_order.append(1)

                    pair[1].side_balance += (-1)
                    pair[1].side_order.append(-1)
                else:
                    pair[0].side_balance += -1
                    pair[0].side_order.append(-1)

                    pair[1].side_balance += 1
                    pair[1].side_order.append(1)

    def sim_match(self, pairing):
        p1 = pairing[0]
        p2 = pairing[1]

        if p1.score != p2.score:
            if p1.score < p2.score:
                p1.paired_up += 1
                p2.paired_down += 1
            else:
                p1.paired_down += 1
                p2.paired_up += 1

        win_percent = p1.str/(p1.str + p2.str)
        roll = random.random()
        
        if win_percent > roll:
            p1.record_match(p2.id, 1)
            p2.record_match(p1.id, 0)
        else:
            p1.record_match(p2.id,0)
            p2.record_match(p1.id,1)
    
    def sim_round(self):
        self.round += 1
        self.find_pairings()
        for pair in self.pairings:
            self.sim_match(pair)
        self.compute_sos()
        
    
    def sim_tournament(self, n_rounds):
        while self.round < n_rounds:
            self.sim_round()

    def compute_sos(self):
        for player in self.player_list:
            opponent_total_score = 0
            opponents_games_played = 0
            for opponent_id in player.opponent_list:
                opponent = next((opponent for opponent in self.player_list if opponent.id == opponent_id),None)
                opponent_total_score += opponent.score
                opponents_games_played += len(opponent.opponent_list)
            player.sos = opponent_total_score/opponents_games_played


    def random_Swiss_weights(self,player_one_index, player_two_index):
        side_penalty = self._compute_side_penalty(player_one_index, player_two_index)
        score_penalty = self._compute_score_penalty(player_one_index, player_two_index)
        random_weight = random.randint(0,100)
        return self.LARGE_CONSTANT-(side_penalty+score_penalty+random_weight)

    def almafi_weights(self,player_one_index, player_two_index):
        side_penalty = self._compute_side_penalty(player_one_index, player_two_index)
        almafi_weight = self._almafi_penalty(player_one_index, player_two_index)
        return self.LARGE_CONSTANT - (side_penalty + almafi_weight)

    algorithms = {
        "random_swiss": random_Swiss_weights,
        "almafi": almafi_weights
    }
    
    def _compute_side_penalty(self, player_one_index, player_two_index):
        player_one, player_two = self.player_list[player_one_index], self.player_list[player_two_index]

        if player_one.side_balance * player_two.side_balance > 0:
            exponent = min(abs(player_one.side_balance),abs(player_two.side_balance))
            return 25*(8**exponent)
        else:
            return 0

    def _compute_score_penalty(self, player_one_index, player_two_index):
        return 75 * abs(self.player_list[player_one_index].score - self.player_list[player_two_index].score)

    def _almafi_penalty(self, player_one_index, player_two_index):
        return (self.round - abs(player_one_index - player_two_index))*200