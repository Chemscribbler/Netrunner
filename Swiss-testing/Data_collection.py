from Tournament import Tournament
from Player import Player
import csv
import random
import cProfile
import re

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
            if i % (num_tests/10) == 0:
                print(".")
        print("Done")


def testing_single_swiss(num_tests, player_list, num_rounds, score_factor=100, side_balance=0.5):
    for i in range(num_tests):
        t = construct_tournament(player_list)
        t.score_factor = score_factor
        t.sim_tournament(num_rounds,side_balance=side_balance)
        ranked_players = rank_results(t)
        for j in range(len(ranked_players)):
            ranked_players[j].finish[j] += 1
            ranked_players[j].final_side_balance.append(ranked_players[j].side_balance) 
        for player in players:
            player.reset_stats()
        if i % (num_tests/10) == 0:
                print(".",end="")
    print("Done")

def testing_double_swiss(num_tests, player_list, num_rounds, score_factor=600, side_balance=0.5):
    for i in range(num_tests):
        t = construct_tournament(player_list)
        t.score_factor = score_factor
        t.sim_dss_tournament(num_rounds,side_balance=side_balance)
        ranked_players = rank_results(t)
        for j in range(len(ranked_players)):
            ranked_players[j].finish[j] += 1
            ranked_players[j].final_side_balance.append(ranked_players[j].side_balance) 
        for player in players:
            player.reset_stats()
        if i % (num_tests/10) == 0:
                print(".",end="")
    print("Done")

def results_collation(player_list, num_sims, file_name):
    with open(f"{file_name}.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile)
        results_writer.writerow(['PID','Str','Top 8 Finish', 'Pair Up/Down','Greater than 1 Pair Up/Down','Unbalanced Sides'])
        for player in player_list:
            count = player.final_side_balance.count(0)
            top_eight = 0
            for i in range(8):
                top_eight += player.finish[i]
            results_writer.writerow([player.id,player.str,top_eight,(player.paired_up+player.paired_down),player.pairing_diff - (player.paired_up+player.paired_down),num_sims-count])
            # print(f"PID:{player.id} Str:{player.str} Unbalnced:{num_sims-count} Top8:{top_eight} OffPairing:{(player.paired_up+player.paired_down)} PairingDist:{player.pairing_diff - (player.paired_up+player.paired_down)}")

def reset_counter_stats(player_list):
    for player in player_list:
        player.finish = [0]*len(player_list)
        player.final_side_balance = []
        player.paired_up = 0
        player.paired_down = 0
        player.pairing_diff = 0


if __name__ == "__main__":
    players = tilted_strength(128,0.5)
    num_sims = 100
    # with open("dist_2.csv",'w',newline='') as csv_file:
    #     writer = csv.writer(csv_file)
    #     for player in players:
    #         writer.writerow([player.id, player.str])

     
    # subset = random.sample(players,32)
    
    num_rounds = 8
    reset_counter_stats(players)
    cProfile.run('testing_double_swiss(num_sims,players,num_rounds)',sort='cumulative')
    
    # results_collation(players,num_sims, "5000_dss_8_rounds")

    # num_rounds = 4
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=600)
    # results_collation(players,num_sims, "10000_sss_4_rounds")
    
    # num_rounds = 5
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=600)
    # results_collation(players,num_sims, "10000_sss_5_rounds")
    
    # num_rounds = 6
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=600)
    # results_collation(players,num_sims, "5000_sss_6_rounds_sf_600")
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=450)
    # results_collation(players,num_sims, "5000_sss_6_rounds_sf_450")
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=200)
    # results_collation(players,num_sims, "5000_sss_6_rounds_sf_200")

    # num_rounds = 7
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=600)
    # results_collation(players,num_sims, "10000_sss_7_rounds")
    
    # num_rounds = 8
    # reset_counter_stats(players)
    # testing_single_swiss(num_sims,players,num_rounds,score_factor=600)
    # results_collation(players,num_sims, "10000_sss_8_rounds")
    
