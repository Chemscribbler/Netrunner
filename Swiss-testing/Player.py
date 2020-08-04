import random
import math

class Player():
    next_id = 0
    
    def __init__(self, str= None, scaler=1):
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
        self.opponent_list = []

        #Side order
        self.side_order = []

        #Results list
        self.results_list = []
        self.score = 0
        self.sos = 0
        self.ext_sos = 0
        self.is_floater = False


    def __repr__(self):
        return f"PID{self.id}"

    def __str__(self):
        return f"PID{self.id}: {self.score} {self.sos}"

    def record_match(self, opp_id, side_given, result):
        self.opponent_list.append(opp_id)
        self.side_order.append(side_given)
        self.side_order.append(side_given)
        self.side_balance += side_given
        self.score += result*3
        


def gen_str(scaler):
    rand = random.random()
    if rand == 0:
        return 0
    else:
        return scaler*math.exp((-1)*scaler*rand)

# [print(player) for player in [Player() for x in range(20)]]
