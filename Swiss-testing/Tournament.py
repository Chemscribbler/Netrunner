import Player
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
        self._next_unpaired_group = 0 #score integer
        self._pair_lowest_next = False
        self.round_paired = False

    
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
        self.setup_next_network()
        
    
    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        else:
            if player.id in [x.id for x in self.player_list]:
                raise ValueError("Player already in Tournament")
            else:
                self.player_list.append(player)
    
    def construct_network(self,algorithm="random_swiss",iterate=True):
        active_group = self._score_groups[self._next_unpaired_group]
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
                    edge_weight = self.algorithms[algorithm](self,active_group, i, j)
                    new_graph.add_edge(active_group[i],active_group[j],weight = edge_weight)

        self._active_pairing_graph = new_graph
        
        if iterate:  
            self.setup_next_network()
    
    
    def setup_next_network(self): 
        try:       
            if self._pair_lowest_next:
                self._next_unpaired_group = self._unpaired_groups.pop(-1)
            else:
                self._next_unpaired_group = self._unpaired_groups.pop(0)
        except IndexError:
            self.round_paired = True
        self._pair_lowest_next = not self._pair_lowest_next
    
    def random_Swiss_weights(self,active_group,player_one_index, player_two_index):
        player_one = active_group[player_one_index]
        player_two = active_group[player_two_index]

        if player_one.id in player_two.opponent_list:
            return 0

        old_floater_penalty = self.compute_old_floater_penalty(player_one, player_two, player_one_index, player_two_index)
        
        
        new_floater_penalty = 10 * (player_one_index + player_two_index)

        side_penalty = self.compute_side_penalty(player_one, player_two)

        random_weight = random.randint(0,10)

        return 10000-(old_floater_penalty+new_floater_penalty+side_penalty+random_weight)


        

    def high_low_swiss_weights(self,active_group, player_one_index, player_two_index):
        pass

    def halfs_swiss_weights(self,active_group, player_one_index, player_two_index):
        pass

    def almafi_weights(self,active_group,player_one_index, player_two_index):
        pass

    algorithms = {
        "random_swiss": random_Swiss_weights,
        "high_low_swiss": high_low_swiss_weights,
        "halfs_swiss": halfs_swiss_weights,
        "almafi": almafi_weights
    }

    def compute_old_floater_penalty(self,player_one, player_two, player_one_index, player_two_index):
        if player_one.score == player_two.score:
            return 0
        else:
            return 25*(player_one.score - player_two.score)*abs(player_one_index - player_two_index)-500
    
    def compute_side_penalty(self, player_one, player_two):
        if player_one.side_balance * player_two.side_balance > 0:
            return 25*(8^(min(abs(player_one.side_balance),abs(player_two.side_balance))))
        else:
            return 0
