import Player

class Tournament():

    def __init__(self):
        self.player_list = []
        self._score_groups = {}
        self.round = 0
    
    def find_pairing_groups(self):
        self._score_groups = {}

        for player in self.player_list:
            try:
                self._score_groups[player.score].append(player.id)
            except:
                self._score_groups[player.score] = [player.id]
    
    def add_player(self, player):
        if self.round != 0:
            raise ValueError("Tried to add a player after Tournament Start")
        else:
            if player.id in [x.id for x in self.player_list]:
                raise ValueError("Player already in Tournament")
            else:
                self.player_list.append(player)