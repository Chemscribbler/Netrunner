from datetime import date
import csv
try:
    from ..core.Player import Player
    from ..core.Tournament import Tournament
except ImportError:
    from Player import Player
    from Tournament import Tournament

class Manager(object):
    """
    Manager object for Single Sides Swiss Tournament
    """

    def __init__(self):
        self.tournament_dict = {}
        self.active_tournament = None
        self.active_tournament_key = None
        self.organizer = 'SASS'


    def create_tournament(self, id):
        try:
            self.tournament_dict[id]
            raise ValueError("Non-unique Tournament ID")
        except KeyError:
            pass

        self.tournament_dict[id] = Tournament()
        self.active_tournament = self.tournament_dict[id]
        self.active_tournament_key = id
    
    def add_player(self, plr_name, **kwargs):
        """
        Add a player to the active tournament, names must be unique
        """
        plr = Player(plr_name, **kwargs)
        self.active_tournament.add_player(plr)
        return plr

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
    
    def _rank_players(self):
        players = self.active_tournament.player_dict.values()
        plr_list = [plr for plr in players]
        for plr in self.active_tournament.dropped_players.values():
            plr_list.append(plr)
        plr_list.sort(key = lambda player: player.sos, reverse=True)
        plr_list.sort(key = lambda player: player.score, reverse=True)
        return plr_list

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
        for plr in self._rank_players():
            print(plr)

    def _gui_return_rankings(self):
        """
        Iterable that returns players in descending rank order (Score > SoS > ???)
        """
        for plr in self._rank_players():
            if not plr.name == "Bye":
                yield plr

    def _gui_return_pairings(self):
        """
        Iterable that returns table pairs
        """
        highest_table = 1
        player_to_tables = {}
        tables_to_players = {}
        t = self.active_tournament
        for plr in self._rank_players():
            try:
                player_to_tables[plr.id]
            except KeyError:
                for pair in t.pairings:
                    if pair[0] == plr.id or pair[1] == plr.id:
                        player_to_tables[pair[0]] = highest_table
                        player_to_tables[pair[1]] = highest_table
                        tables_to_players[highest_table] = pair
                        highest_table += 1
                        break
        for table, pair in tables_to_players.items():
            if t.player_dict[pair[0]].round_dict[t.round]['side'] > 0:
                yield (table,pair[0],pair[1])
            else:
                yield (table,pair[1],pair[0])


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

    def pair_round(self,display=True):
        """
        Pairs round automatically- should allow for people to rematch with opposite sides
        """
        t = self.active_tournament
        # if not self.check_round_done():
        #     raise ValueError("Not all pairs have reported")
        t.round += 1
        t.make_initial_graph()
        iteration = 1
        while not t.pairings_done:
            print(iteration)
            iteration += 1
            t.make_pairings()
            t.test_pairings()
        # print(t.player_dict)
        # t.make_pairings()
        t.assign_sides()
        if display:
            print(f"Pairing Result {t.test_pairings()}")
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
        self.compute_ext_sos()
        if display_rankings:
            self.display_rankings()
        if pair_next:
            self.pair_round()
    
    def compute_sos(self):
        for player in self.active_tournament.player_dict.values():
            opponent_total_score = 0
            opponents_games_played = 0
            for rnd in player.round_dict.values():
                try:
                    opponent = self.active_tournament.player_dict[rnd['opp_id']]
                    if opponent.name == 'Bye':
                        continue
                except KeyError:
                    try:
                        opponent = self.active_tournament.dropped_players[rnd['opp_id']]
                        if opponent.name == 'Bye':
                            continue
                    except:
                        continue
                opponent_total_score += opponent.score
                opponents_games_played += len(opponent.round_dict)
            if opponents_games_played == 0:
                #Handling div by 0 issues
                opponents_games_played = 1
            player.sos = opponent_total_score/opponents_games_played

    def compute_ext_sos(self):
        for player in self.active_tournament.player_dict.values():
            opponents_total_sos = 0
            opponents_games_played = 0
            for rnd in player.round_dict.values():
                try:
                    opponent = self.active_tournament.player_dict[rnd['opp_id']]
                    if opponent.name == 'Bye':
                        continue
                except KeyError:
                    try:
                        opponent = self.active_tournament.dropped_players[rnd['opp_id']]
                        if opponent.name == 'Bye':
                            continue
                    except:
                        continue
                opponents_total_sos += opponent.sos
                opponents_games_played += len(opponent.round_dict)
            if opponents_games_played == 0:
                #Handling div by 0 issues
                opponents_games_played = 1
            player.ext_sos = opponents_total_sos/opponents_games_played


    def backup(self,path=None): 
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

    def export_json(self):
        """
        Creates json that matches ABR format
        """
        json = {
            'name': self.active_tournament_key,
            'date': date.today().strftime("%Y-%m-%d"),
            'cutToTop': 0,
            'preliminaryRounds': 0,
            'tournamentOrganiser':{
                'nrdbId':'',
                'nrdbUsername':self.organizer
            },
            'players': {},
            'eliminationPlayers':{},
            'uploadedFrom':'SASS',
            'links': {0: {'rel':'schemaderivedfrom','href':"http://steffens.org/nrtm/nrtm-schema.json"},
                      1: {'rel':'uploadedfrom','href':'https://github.com/Chemscribbler/Netrunner/tree/main/SingleSided_App'}}
        }

        player_list = self._rank_players()
        for i, plr in enumerate(player_list):
            json['players'][i] = {
                'id':plr.id,
                'name':plr.name,
                'rank':i,
                'corpIdentity':plr.corp_id,
                'runnerIdentity':plr.runner_id,
                'matchPoints':plr.score,
                'strengthOfSchedule':str(round(plr.sos,4)),
                'extendedStrengthOfSchedule':str(round(plr.ext_sos,6))
            }
        
        return json

    def export_standings_csv(self,file_path=None):
        player_list = self._rank_players()
        if not file_path:
            file_path = f"{self.active_tournament_key}.csv"
        with open(file_path,'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name",'ID','Score','SoS','Ext. SoS', 'Side Balance', 'Corp ID', "Runner ID"])
            for plr in player_list:
                writer.writerow([plr.name, plr.id, plr.score,plr.sos,plr.ext_sos, plr.side_balance, plr.corp_id, plr.runner_id])
    
    def export_pairings_csv(self,file_path=None):
        pairings_iter = self._gui_return_pairings()
        with open(file_path,'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow('Table',"Corp Player",'Runner Player')
            for pair in pairings_iter:
                writer.writerow([pair[0],pair[1],pair[2]])



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