from Matrix_Tourn import Tourney
from Player import Player
import csv
import random
from Data_collection import tilted_strength, even_strength, rank_results
from time import time
import cProfile

def construct_tourney(player_list,**kwargs):
    t = Tourney()
    for player in player_list:
        t.add_player(player)
    return t

def reset_counter_stats(player_list):
    for player in player_list:
        player.finish = [0]*len(player_list)
        player.final_side_balance = []
        player.off_pair = 0
        player.pairing_diff = 0

def rank_list(player_list):
    player_list.sort(key= lambda x: x.sos,reverse=True)
    player_list.sort(key= lambda x: x.score, reverse=True)
    return player_list

def display_pairings(tourney):
    p1_list = []
    for pair in tourney.pairings:
        p1_list.append(pair[0])
    rank_list(p1_list)
    print("ID:Score:Side Balance -- ID:Score:Side Balance")
    for p1 in p1_list:
        for pair in tourney.pairings:
            if p1 == pair[0]:
                p2 = pair[1]
                print(f"{p1.id}:{p1.score}:{p1.side_balance} -- {p2.id}:{p2.score}:{p2.side_balance}")
                break

 
def test_tournament_conditions(num_tests, player_list, num_rounds, score_factor=200, double_sided=False):
    for i in range(num_tests):
        t = construct_tourney(player_list)
        t.score_factor = score_factor
        t.sim_tourney(num_rounds, double_sided=double_sided)
        ranked_players = rank_list([player for player in t.player_dict.values()])
        for index, player in enumerate(ranked_players):
            player.finish[index] += 1
            player.final_side_balance.append(player.side_balance)
        for player in t.player_dict.values():
            player.reset_stats()
        if i % (num_tests/10) == 0:
            print(".",end="")
    print("Done")

def results_collation(player_list, num_sims, file_name, top_x=8):
    with open(f"{file_name}.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile)
        results_writer.writerow(['PID','Str',f'Top {top_x} Finish', 'Pair Up/Down','Greater than 1 Pair Up/Down','Unbalanced Sides'])
        for player in player_list:
            count = player.final_side_balance.count(0)
            top_x_count = 0
            for i in range(top_x):
                top_x_count += player.finish[i]
            results_writer.writerow([player.id,player.str,top_x_count,player.off_pair,player.pairing_diff-player.off_pair,num_sims-count])

def pair_looper(tourney):
    for pair in tourney.pairings:
        tourney.sim_match(pair)

if __name__ == "__main__":
    random.seed()
    players = tilted_strength(128,0.5)
    num_sims = 100

    t = construct_tourney(players)
    # t.pairings = []
    # players_copy = players
    # random.shuffle(players_copy)
    # while players_copy:
    #     t.pairings.append((players_copy.pop().id, players_copy.pop().id))
    # # t.make_pairings()
    # # print(t.player_dict)
    # cProfile.run("pair_looper(t)")
    tic = time()
    num_rounds = 8
    reset_counter_stats(players)
    test_tournament_conditions(num_sims,players,num_rounds,double_sided=True)
    results_collation(players,num_sims,f"{num_sims}_dss_{num_rounds}_rnds_{len(players)}_plrs")
    print((time()-tic)/60)
    
    tic = time()
    score_factor = 200
    num_rounds = 8
    reset_counter_stats(players)
    test_tournament_conditions(num_sims,players,num_rounds,score_factor=score_factor)
    results_collation(players,num_sims,f"{num_sims}_sss_{num_rounds}_rnds_{len(players)}_plrs_{score_factor}_sf")
    print((time()-tic)/60.0)

    # tic = time()
    # num_rounds = 6
    # reset_counter_stats(players)
    # test_tournament_conditions(num_sims,players,num_rounds,score_factor=score_factor)
    # results_collation(players,num_sims,f"{num_sims}_sss_{num_rounds}_rnds_{len(players)}_plrs_{score_factor}_sf")
    # print((time()-tic)/60.0)

    # tic = time()
    # num_rounds = 8
    # reset_counter_stats(players)
    # test_tournament_conditions(num_sims,players,num_rounds,score_factor=score_factor)
    # results_collation(players,num_sims,f"{num_sims}_sss_{num_rounds}_rnds_{len(players)}_plrs_{score_factor}_sf")
    # print((time()-tic)/60.0)
