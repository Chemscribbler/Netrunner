from Player import Player
import Tournament
import csv


class Manager(object):
    """
    Manager object for Single Sides Swiss Tournament
    """

    def __init__(self):
        self.tournament_dict = {}
        self.active_tournament = None
        self.active_tournament_key = None

    def create_tournament(self, id):
        try:
            self.tournament_dict[id]
            raise ValueError("Non-unique Tournament ID")
        except KeyError:
            pass

        self.tournament_dict[id] = Tournament.Tournament()
        self.active_tournament = self.tournament_dict[id]
        self.active_tournament_key = id
    
    def add_player(self, plr_name, **kwargs):
        """
        Add a player to the active tournament, names must be unique
        """
        plr = Player(plr_name, **kwargs)
        self.active_tournament.add_player(plr)

    def drop_player(self, player_name):
        """
        Drop a player from the active tournament and add/remove a bye player as needed
        player_name: The text name for the player
        returns true if successful
        """
        player = None
        for plr in self.active_tournament.player_dict.values():
            if plr.name == player_name:
                player = plr
                break
        if not player:
            print(f"{player_name} is not in the current list")
            return False
        return self.active_tournament.drop_player(player)
        

    
    def start_tournament(self):
        """
        Closes registration and makes first round pairings
        """
        self.active_tournament.start_tourney()
        self.display_pairings()
    
    def display_pairings(self):
        """
        Utility function for showing pairings
        Displays Player Name, ID, their side and the same for their opponent
        """
        t = self.active_tournament
        for pair in t.pairings:
            p1 = t.player_dict[pair[0]]
            p2 = t.player_dict[pair[1]]
            print(f"{p1.name}, ID:{p1.id} as {self.display_side_name(p1.round_dict[t.round]['side'])} vs {p2.name}, ID:{p2.id} as {self.display_side_name(p2.round_dict[t.round]['side'])}")

    def display_rankings(self):
        """
        Utility function for showing standings.
        Columns are Player_ID, Name, Score, SoS, and Side Balance
        """
        players = self.active_tournament.player_dict.values()
        plr_list = [plr for plr in players]
        for plr in self.active_tournament.dropped_players.values():
            plr_list.append(plr)
        plr_list.sort(key = lambda player: player.sos, reverse=True)
        plr_list.sort(key = lambda player: player.score, reverse=True)
        for plr in plr_list:
            print(plr)

    def display_side_name(self,side_value):
        if side_value < 0:
            return "Runner"
        elif side_value > 0:
            return "Corp"
        else:
            return "None"
        

    def record_result(self, p1_id, p2_id, p1_points, p2_points):
        """
        Use to record/report a match result.
        p1_id: the numeric id of either player
        p2_id: the numeric id of the other player
        p1_points: Number of points p1 recieves (should be 3/1/0)
        p2_points: Number of points p1 recieves (should be 3/1/0)
        """
        p1 = self.active_tournament.player_dict[p1_id]
        p2 = self.active_tournament.player_dict[p2_id]
        rnd = self.active_tournament.round

        if p1.round_dict[rnd]["opp_id"] != p2_id:
            raise ValueError(f"Players ({p1.name}, {p2.name}) are not playing this round")
        try:
            p1.round_dict[rnd]['result']
            raise ValueError(f"Players ({p1.name}, {p2.name}) already have a recorded result, did you mean 'ammend_result'?")
        except KeyError:
            pass

        p1.record_result(rnd, p1_points)
        p2.record_result(rnd, p2_points)
    
    def ammend_result(self, p1_id, p2_id, p1_points, p2_points):
        """
        Use to ammend a match result.
        p1_id: the numeric id of either player
        p2_id: the numeric id of the other player
        p1_points: Number of points p1 recieves (should be 3/1/0)
        p2_points: Number of points p1 recieves (should be 3/1/0)
        """
        p1 = self.active_tournament.player_dict[p1_id]
        p2 = self.active_tournament.player_dict[p2_id]
        rnd = self.active_tournament.round

        if p1.round_dict[rnd]["opp_id"] != p2_id:
            raise ValueError(f"Players ({p1.name}, {p2.name}) are not playing this round")

        p1.ammend_result(rnd, p1_points)
        p2.ammend_result(rnd, p2_points)


    def check_round_done(self):
        """
        Utility function to test if all pairs in the given round have reported results
        If it returns 'True' the round is done
        Otherwise it will return false and print a message for each player
        """
        exceptions = 0
        for plr in self.active_tournament.player_dict.values():
            try:
                plr.round_dict[self.active_tournament.round]["result"]
            except KeyError:
                print(f"Player {plr.name} does not have a recorded result for this round {self.active_tournament.round}")
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
        t = self.active_tournament
        if not self.check_round_done():
            raise ValueError("Not all pairs have reported")
        t.round += 1
        t.make_initial_graph()
        while not t.pairings_done:
            t.make_pairings()
            t.test_pairings()
        t.make_pairings()
        print(f"Pairing Result {t.test_pairings()}")
        t.assign_sides()
        self.display_pairings()
    
    def finish_round(self,pair_next=True,display_rankings=True):
        """
        Checks that the round is done, and depending on optional arguments, starts next round
        pair_next: If True (default) will pair the next round, otherwise leave the round unpaired (can pair with pair_round)
        display_rankings: If true (default) will print current standings
        """
        if not self.check_round_done():
            raise ValueError("Not all pairs have reported")
        self.compute_sos()
        if display_rankings:
            self.display_rankings()
        if pair_next:
            self.pair_round()
    
    def compute_sos(self):
        for player in self.active_tournament.player_dict.values():
            opponent_total_score = 0
            opponents_games_played = 0
            for rnd in player.round_dict.values():
                opponent = self.active_tournament.player_dict[rnd['opp_id']]
                opponent_total_score += opponent.score
                opponents_games_played += len(opponent.round_dict)
            player.sos = opponent_total_score/opponents_games_played

    def backup(self): 
        """
        Creates a series of .csv files to store results and player records
        """
        for plr in self.active_tournament.player_dict.values():
            with open(f"{self.active_tournament_key}_{plr.name}.csv", 'w',newline='') as csvfile:
                plr_writer = csv.writer(csvfile)
                plr_writer.writerow(["Opp_ID, Side, Result"])
                for rnd, entry in plr.round_dict.items():
                    try:
                        row = [rnd, entry["opp_id"], entry["side"],entry['result']]
                    except KeyError:
                        row = [rnd, entry["opp_id"], entry["side"]]
                    plr_writer.writerow(row)
        
        with open(f"{self.active_tournament_key}.csv",'w',newline='') as csvfile:
            rank_writer = csv.writer(csvfile)
            players = self.active_tournament.player_dict.values()
            plr_list = [plr for plr in players if plr.name != "Bye"]
            plr_list.sort(key = lambda player: player.sos, reverse=True)
            plr_list.sort(key = lambda player: player.score, reverse=True)
            for entry in plr_list:
                rank_writer.writerow([entry.name, entry.id, entry.score, entry.sos, entry.side_balance])

    def test_players(self, count):
        name_list = ["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliett", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]
        for i in range(count):
            self.add_player(name_list[i])

    def sim_round(self):
        for pair in self.active_tournament.pairings:
            if pair[0] * pair[1] < 0:
                if pair[0] == -1:
                    self.record_result(pair[0], pair[1], 0, 3)
                else:
                    self.record_result(pair[0], pair[1], 3, 0)
            self.record_result(pair[0], pair[1], 3, 0)


    def help(self):
        with open("help.txt", 'r') as f:
            print(f.read())

if __name__ == "__main__":
    m = Manager()
    t_name =input("Tournament Name: ")
    m.create_tournament(t_name)
    print("Add players by typing m.add_player('#NAME'), when finished type m.start_tournament()")
    print("Report results with m.record_result(...) and finish a round with m.finish_round()")
    print("Type m.help() for more directions, or help(m.command())")