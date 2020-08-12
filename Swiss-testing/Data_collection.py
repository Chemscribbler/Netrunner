from Tournament import Tournament
from Player import Player
import csv

def even_strength(player_count):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(str=1))
    return player_list

def tilted_strength(player_count):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(scaler=10))
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

def testing(num_tests, num_players, num_rounds,test_name='even_test'):

    tests = {
    'even_test':even_strength,
    'biased': tilted_strength
    }

    with open("results.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile)
        players = tests[test_name](num_players)
        results_writer.writerow([f"PID{player.id}:{player.str}" for player in players])

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


if __name__ == "__main__":
    # even_testing(100)
    testing(1000,32,6,'biased')