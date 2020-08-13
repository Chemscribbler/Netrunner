from Tournament import Tournament
from Player import Player
import csv

def even_strength(player_count):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(str=1))
    return player_list

def tilted_strength(player_count, scalar=1):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(scaler=scalar))
    player_list.sort(key= lambda player: player.str, reverse=True)
    for i in range(len(player_list)):
        player_list[i].id = i
    return player_list


def rank_results(tournament):
    tournament.player_list.sort(key= lambda player: player.sos, reverse=True)
    tournament.player_list.sort(key = lambda player: player.score, reverse=True)
    return tournament.player_list

def construct_tournament(player_list):
    t = Tournament()
    for player in player_list:
        t.add_player(player)
    return t

def testing(num_tests, num_players, num_rounds,test_name='even_test',file_name='results'):

    tests = {
    'even_test':even_strength,
    'biased': tilted_strength
    }

    with open(f"{file_name}.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile,delimiter=';')
        players = tests[test_name](num_players)
        results_writer.writerow([f"PID{player.id}:{player.str}: {player.side_balance}" for player in players])

        for i in range(num_tests):
            t = construct_tournament(players)
            t.sim_tournament(num_rounds)
            ranked_players = rank_results(t)
            results_writer.writerow(ranked_players)
            for player in ranked_players:
                player.reset_stats()
            if i % 100 == 0:
                print(".")
        print("Done")

def testing_defined_players(num_tests, player_list, num_rounds, file_name='results'):
    for _ in range(num_tests):
        t = construct_tournament(player_list)
        t.sim_tournament(num_rounds)
        ranked_players = rank_results(t)
        for j in range(len(ranked_players)):
            ranked_players[j].finish[j] += 1
            ranked_players[j].final_side_balance.append(ranked_players[j].side_balance) 
        for player in players:
            player.reset_stats()

    return player_list

if __name__ == "__main__":
    players = tilted_strength(32,6)
    num_sims = 1000
    num_rounds = 6
    for player in players:
        player.finish = [0]*32
        player.final_side_balance = []
    testing_defined_players(num_sims,players,num_rounds)
    [print(player.finish) for player in players]
    for player in players:
        count = player.final_side_balance.count(0)
        top_eight = 0
        for i in range(8):
            top_eight += player.finish[i]
        print(f"PID:{player.id} Str:{player.str} Unbalnced:{num_sims-count} Top8:{top_eight} OffPairing:{(player.paired_up+player.paired_down)/(num_sims*num_rounds)*100}")


    # even_testing(100)
    # testing(5000,32,4,'biased',"4_biased_rounds")
    # testing(5000,32,5,'biased',"5_biased_rounds")
    # testing(5000,32,6,'biased',"6_biased_rounds")
    # testing(5000,32,6,'biased',"7_biased_rounds")
    # testing(5000,32,8,"biased","8_biased_rounds")