import random
import math

class Player():
    next_id = 0
    
    def __init__(self, str= None, scaler=1, score=0, sos=0):
        if str is not None:
            self.str = str
        else:
            self.str = gen_str(scaler)

        self.id = Player.next_id
        Player.next_id += 1

        #Positive is more corp games, negative is more runner
        self.side_balance = 0

        #Opponents
        #Each match gets an entry in the list
        self.opponent_dict = {}

        #Side order
        self.side_order = {}

        self.side = 0

        #Results list
        self.results_dict = {}
        self.score = score
        self.sos = sos
        self.ext_sos = 0

        self.off_pair = 0
        self.pairing_diff = 0

        self.round_dictionary = {}


    def __repr__(self):
        return f"PID{self.id}"

    def __str__(self):
        return f"PID{self.id}: {self.score} {self.sos}"

    def record_match(self, opp_id, result, round):
        self.opponent_dict[round]=opp_id
        self.score += result
        self.results_dict[round] = result
        self.side_order[round] = self.side
        self.side_balance += self.side

    def reset_stats(self):
        self.side_balance = 0
        self.opponent_dict = {}
        self.side_order = {}
        self.results_dict = {}
        self.score = 0
        self.sos = 0
        self.ext_sos = 0
        self.is_floater = False


def gen_str(scaler):
    return random.lognormvariate(mu=0.5,sigma=scaler)

# [print(player) for player in [Player() for x in range(20)]]
