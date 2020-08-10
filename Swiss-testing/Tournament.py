from Player import Player
import networkx as nx
import random

class Tournament():

    def __init__(self):
        self.player_list = []
        self._score_groups = {}
        self.round = 0
        self.pairings = {}
        self._active_pairing_graph = nx.Graph()
        self._unpaired_groups = []
        self._pairing_group_score = 0 #score integer
        self._pair_lowest_next = False
        self.round_paired = False
        self.LARGE_CONSTANT = 10000
        self.bye_player = Player(0)

    
    def find_pairing_groups(self):
        self._score_groups = {}
        self._unpaired_groups = []
        self._pair_lowest_next = False

        for player in self.player_list:
            try:
                self._score_groups[player.score].append(player)
            except:
                self._unpaired_groups.append(player.score)
                self._score_groups[player.score] = [player]
        
        self._unpaired_groups.sort(reverse=True)
        self._pairing_group_score = self._unpaired_groups[0]
        # self.choose_next_pairing_group()
        
    
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
        active_group = self._score_groups[self._pairing_group_score]
        new_graph = nx.Graph()

        #Sort by SoS then Score to deal with floaters
        active_group.sort(key= lambda player: player.sos, reverse=True)
        active_group.sort(key = lambda player: player.score, reverse=True)

        for player in active_group:
            new_graph.add_node(player)


        for i in range(len(active_group)):
            for j in range(len(active_group)):
                if i >= j:
                    pass
                else:
                    if active_group[i].id in active_group[j].opponent_list:
                        edge_weight = 0
                    else:
                        edge_weight = self.algorithms[algorithm](self,active_group, i, j, round = self.round)
                    new_graph.add_edge(active_group[i],active_group[j],weight = edge_weight)

        self._active_pairing_graph = new_graph
        
        if iterate:  
            self.choose_next_pairing_group()    

    def choose_next_pairing_group(self): 
        try:       
            if self._pair_lowest_next:
                self._pairing_group_score = self._unpaired_groups.pop(-1)
            else:
                self._pairing_group_score = self._unpaired_groups.pop(0)
        except IndexError:
            self.round_paired = True
        self._pair_lowest_next = not self._pair_lowest_next

    def find_pairings(self, algorithm="random_swiss",**kwargs):
        self.construct_network(algorithm=algorithm,**kwargs)
        self.pairings[self._pairing_group_score] = nx.max_weight_matching(self._active_pairing_graph)

        self.choose_next_pairing_group()
        if not self.round_paired:
            self.find_pairings(algorithm=algorithm, **kwargs)
        else:
            # print(self.pairings)
            return
        
    
    def _constant_weights(self, active_group, player_one_index, player_two_index):
        player_one = active_group[player_one_index]
        player_two = active_group[player_two_index]

        old_floater_penalty = self._compute_old_floater_penalty(player_one, player_two, player_one_index, player_two_index)
        new_floater_penalty = self._compute_new_floater_penalty(player_one_index, player_two_index)
        side_penalty = self._compute_side_penalty(player_one, player_two)
        return old_floater_penalty+new_floater_penalty+side_penalty

    def random_Swiss_weights(self,active_group,player_one_index, player_two_index, **kwargs):
        constant_penalties = self._constant_weights(active_group, player_one_index, player_two_index)
        random_weight = random.randint(0,100)
        return self.LARGE_CONSTANT-(constant_penalties+random_weight)

    def high_high_swiss_weights(self,active_group,player_one_index, player_two_index, **kwargs):
        constant_penalties = self._constant_weights(active_group, player_one_index, player_two_index)
        distance_penalty = self._high_high_penalty(active_group, player_one_index, player_two_index)
        return self.LARGE_CONSTANT - (constant_penalties + distance_penalty)

    def high_low_swiss_weights(self,active_group,player_one_index, player_two_index, **kwargs):
        constant_penalties = self._constant_weights(active_group, player_one_index, player_two_index)
        distance_penalty = self._high_low_penalty(active_group,player_one_index, player_two_index)

        return self.LARGE_CONSTANT - (constant_penalties + distance_penalty)

    def halfs_swiss_weights(self,active_group,player_one_index, player_two_index, **kwargs):
        constant_penalties = self._constant_weights(active_group, player_one_index, player_two_index)
        distance_penalty = self._halfway_pairing_penalty(active_group,player_one_index, player_two_index)

        return self.LARGE_CONSTANT - (constant_penalties + distance_penalty)

    def almafi_weights(self,active_group,player_one_index, player_two_index, round):
        pass


    algorithms = {
        "high_high_swiss": high_high_swiss_weights,
        "random_swiss": random_Swiss_weights,
        "high_low_swiss": high_low_swiss_weights,
        "halfs_swiss": halfs_swiss_weights,
        "almafi": almafi_weights
    }

    def _compute_old_floater_penalty(self,player_one, player_two, player_one_index, player_two_index):
        if player_one.score == player_two.score:
            return 0
        else:
            return 25*(player_one.score - player_two.score)*abs(player_one_index - player_two_index)-500

    def _compute_new_floater_penalty(self, player_one_index, player_two_index):
        return 10 * (player_one_index + player_two_index)
    
    def _compute_side_penalty(self, player_one, player_two):
        if player_one.side_balance * player_two.side_balance > 0:
            exponent = min(abs(player_one.side_balance),abs(player_two.side_balance))
            return 25*(8**exponent)
        else:
            return 0

    def _halfway_pairing_penalty(self, active_group, player_one_index, player_two_index):
        if active_group[player_one_index].score != active_group[player_two_index].score:
            return 0
        else:
            count_of_floaters = 0
            for player in active_group:
                if player.is_floater:
                    count_of_floaters += 1
            constant = (len(active_group) - 2*count_of_floaters)/2

            return (constant - abs(player_one_index - player_two_index))**2

    def _high_low_penalty(self, active_group, player_one_index, player_two_index):
        if active_group[player_one_index].score != active_group[player_two_index].score:
            return 0
        else:
            count_of_floaters = 0
            for player in active_group:
                if player.is_floater:
                    count_of_floaters += 1
            return (len(active_group)-count_of_floaters - abs(player_one_index - player_two_index))**2

    def _high_high_penalty(self, active_group, player_one_index, player_two_index):
        if active_group[player_one_index].score != active_group[player_two_index].score:
            return 0
        else:
            return abs(player_one_index - player_two_index)**2

    def _almafi_penalty(self, active_group, player_one_index, player_two_index, round):
        if active_group[player_one_index].score != active_group[player_two_index].score:
            return 0
        else:
            return (round - abs(player_one_index - player_two_index))**2