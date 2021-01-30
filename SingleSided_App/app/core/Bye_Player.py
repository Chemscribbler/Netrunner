from Player import Player

class Bye_Player(Player):
    def __init__(self):
        super().__init__(name = "Bye")
        self.id = -1
        self.score = -5
    
    def __str__(self):
        return "Bye"

    def check_allowed_pairing(self, opp_id, *args, **kwargs):
        for rnd_record in self.round_dict.values():
            if rnd_record["opp_id"] == opp_id:
                return False
            else:
                return True
    
    def record_pairing(self, opp_id, assigned_side, rnd):
        self.round_dict[rnd] = {"opp_id": opp_id, "side": 0}