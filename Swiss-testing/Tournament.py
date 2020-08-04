import Player
import networkx as nx

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
        self._next_unpaired_group = self._unpaired_groups.pop(0)
        
    
    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        else:
            if player.id in [x.id for x in self.player_list]:
                raise ValueError("Player already in Tournament")
            else:
                self.player_list.append(player)
    
    def construct_network(self):
        score_group = self._next_unpaired_group
        new_graph = nx.Graph()
        for player in self._score_groups[score_group]:
            new_graph.add_node(player)
        self._active_pairing_graph = new_graph
        
        self._pair_lowest_next = not self._pair_lowest_next
        if self._pair_lowest_next:
            self._next_unpaired_group = self._unpaired_groups.pop(-1)
        else:
            self._next_unpaired_group = self._unpaired_groups.pop(0)
    
    