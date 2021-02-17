class Player():
    next_id = 0

    def __init__(self, name, corp_id ="NA", runner_id ="NA",earned_bye=False):
        self.id = Player.next_id
        Player.next_id += 1
        self.name = name

        self.corp_id = corp_id
        self.runner_id = runner_id

        #Round dict has 1 entry for every round
        #Every round contains a dictionary of opponent ID, Side Played, and Score
        self.round_dict = {}
        self.score = 0
        self.side_balance = 0
        self.sos = 0
        self.ext_sos = 0

        self.is_bye = False
        self.earned_bye = earned_bye
        self.recieved_bye = False
    
    def __repr__(self):
        return f"PID:{self.id}, {self.name}"
    
    def __str__(self):
        return f"{self.id}:{self.name}- Score:{self.score} SoS:{self.sos} Sides:{self.side_balance}" 
    
    def check_allowed_pairing(self, opp_id, curr_round):
        if self.check_played_twice(opp_id):
            print("Played Twice")
            return False
        if opp_id == -1 and self.recieved_bye:
            print("Already had bye")
            return False
        #Check to see if this is a rematch
        for rnd_record in self.round_dict.values():
            if rnd_record["opp_id"] != opp_id:
                pass
            else:
                #If this is a rematch, does the forced side choice make their side bias worse (provided it's not 0)
                if abs(self.side_balance + self.round_dict[curr_round]['side']) > abs(self.side_balance) and self.side_balance != 0:
                    print("Side would be wrong")
                    return False
                else:
                    return True
        return True
    
    def check_played_twice(self, opp_id):
        count = 0
        for rnd_record in self.round_dict.values():
            if rnd_record['opp_id'] == opp_id:
                try:
                    rnd_record['result']
                    count += 1
                except KeyError:
                    continue
        if count > 1:
            return True
        else:
            return False

    def get_opp_list(self):
        lst = []
        for rnd_values in self.round_dict.values():
            lst.append(rnd_values["opp_id"])
        return lst
    
    def record_pairing(self, opp_id, assigned_side, rnd):
        self.round_dict[rnd] = {"opp_id": opp_id, "side": assigned_side}
    
    def record_result(self,rnd,result):
        self.round_dict[rnd]['result'] = result
        self.score += result
        self.side_balance += self.round_dict[rnd]['side']
    
    def ammend_result(self, rnd, result):
        self.score -= self.round_dict[rnd]['result']
        self.score += result
        self.round_dict[rnd]['result']

    def report_details(self):
        return self.round_dict
    
    def flip_side(self, opp_id):
        for rnd_dict in self.round_dict.values():
            if rnd_dict['opp_id'] == opp_id:
                return rnd_dict['side'] * (-1)

    
    def report_summary(self):
        return {"id": self.id, "score": self.score, "sos":self.side_balance, "side_bal": self.side_balance}

