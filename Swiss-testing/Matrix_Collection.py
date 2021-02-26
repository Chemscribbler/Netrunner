from Matrix_Tourn import Tourney
from Player import Player
import csv
import random
# from Data_collection import tilted_strength, even_strength, rank_results
from time import time
# import cProfile
import pandas as pd
from scipy.stats import pearsonr, combine_pvalues
from numpy import percentile

def even_strength(player_count):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(str=1))
    return player_list

def tilted_strength(player_count, scalar=0.5):
    player_list = []
    for _ in range(player_count):
        player_list.append(Player(scaler=scalar))
    player_list.sort(key= lambda player: player.str, reverse=True)
    for i in range(len(player_list)):
        player_list[i].id = i+1
    return player_list

def rank_results(tournament):
    tournament.player_list.sort(key= lambda player: player.sos, reverse=True)
    tournament.player_list.sort(key = lambda player: player.score, reverse=True)
    return tournament.player_list

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
        p1_list.append(tourney.player_dict[pair[0]])
    rank_list(p1_list)
    print("ID:Score:Side Balance:ID:Score:Side Balance")
    for plr in p1_list:
        for pair in tourney.pairings:
            if plr.id == pair[0]:
                p1 = tourney.player_dict[pair[0]]
                p2 = tourney.player_dict[pair[1]]
                print(f"{p1.id}:{p1.score}:{p1.side_balance} : {p2.id}:{p2.score}:{p2.side_balance}")
                break


def test_single_tournament(player_list, num_rounds, score_factor=2, double_sided=False):
    t = construct_tourney(player_list)
    t.score_factor = score_factor
    t.sim_tourney(num_rounds, double_sided=double_sided)
    ranked_players = rank_list([player for player in t.player_dict.values()])
    for index, player in enumerate(ranked_players):
        player.finish[index] += 1
        player.final_side_balance.append(player.side_balance)

 
def test_tournament_conditions(num_tests, player_list, num_rounds, score_factor=2, double_sided=False,verbose=True):
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
        if i % (num_tests/10) == 0 and verbose:
            print(".",end="")
    print("Done")

def results_collation(player_list, num_sims, file_name, top_x=4):
    with open(f"{file_name}.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile)
        results_writer.writerow(['PID','Str',f'Top {top_x} Finish', 'Pair Up/Down','Greater than 1 Pair Up/Down','Unbalanced Sides'])
        for player in player_list:
            count = player.final_side_balance.count(0)
            top_x_count = 0
            for i in range(top_x):
                top_x_count += player.finish[i]
            results_writer.writerow([player.id,player.str,top_x_count,player.off_pair,player.pairing_diff-player.off_pair,num_sims-count])

def collect_across_distribution(player_count, num_plr_dist, num_sims,\
                                sss_rounds, dss_rounds, player_dist, top_x=4,verbose=True):
    df_dss = pd.DataFrame(0, columns=range(player_count),index=range(player_count))
    df_sss_1 = pd.DataFrame(0, columns=range(player_count),index=range(player_count))
    df_sss_2 = pd.DataFrame(0, columns=range(player_count),index=range(player_count))
    df_sss_3 = pd.DataFrame(0, columns=range(player_count),index=range(player_count))
    df_sss_10 = pd.DataFrame(0, columns=range(player_count),index=range(player_count))

    for _ in range(num_plr_dist):
        timer=time()
        players = player_dist(player_count)

        reset_counter_stats(players)
        test_tournament_conditions(num_sims, players, num_rounds=dss_rounds, double_sided=True, score_factor=3,verbose=verbose)
        temp_df = pd.DataFrame([plr.finish for plr in players]).T
        df_dss += temp_df

        reset_counter_stats(players)
        test_tournament_conditions(num_sims, players, num_rounds=sss_rounds, score_factor=1,verbose=verbose)
        temp_df = pd.DataFrame([plr.finish for plr in players]).T
        df_sss_1 += temp_df

        reset_counter_stats(players)
        test_tournament_conditions(num_sims, players, num_rounds=sss_rounds, score_factor=2,verbose=verbose)
        temp_df = pd.DataFrame([plr.finish for plr in players]).T
        df_sss_2 += temp_df

        reset_counter_stats(players)
        test_tournament_conditions(num_sims, players, num_rounds=sss_rounds, score_factor=3,verbose=verbose)
        temp_df = pd.DataFrame([plr.finish for plr in players]).T
        df_sss_3 += temp_df

        reset_counter_stats(players)
        test_tournament_conditions(num_sims, players, num_rounds=sss_rounds, score_factor=10,verbose=verbose)
        temp_df = pd.DataFrame([plr.finish for plr in players]).T
        df_sss_10 += temp_df

        print((time()-timer)/60)
    
    return [df_dss, df_sss_1, df_sss_2, df_sss_3, df_sss_10]

def test_format_correllation(num_sims, dss_rounds=8, sss_rounds=6, num_players=32, sss_sf=2, shuffle_plrs=True):
    d_error_array = []
    if not shuffle_plrs:
        plr_list = tilted_strength(num_players)
    for i in range(num_sims):
        if shuffle_plrs:
            plr_list = tilted_strength(num_players)
        else:
            for plr in plr_list:
                plr.reset_stats()
        t = construct_tourney(plr_list)
        t.sim_tourney(dss_rounds,double_sided=True)
        results_list = rank_list([plr for plr in t.player_dict.values()])
        for i, player in enumerate(results_list):
            player.finish_one = i+1
        t1_results = [plr.finish_one for plr in plr_list]
        
        for plr in plr_list:
            plr.reset_stats()
        t = construct_tourney(plr_list)
        t.score_factor = sss_sf
        t.sim_tourney(sss_rounds,double_sided=False)
        results_list = rank_list([plr for plr in t.player_dict.values()])
        for i, player in enumerate(results_list):
            player.finish_two = i+1
        t2_results = [plr.finish_two for plr in plr_list]
        
        d_true_vs_dss = pearsonr([x+1 for x in range(num_players)],t1_results)
        d_true_vs_sss = pearsonr([x+1 for x in range(num_players)],t2_results)

        d_error_array.append(d_true_vs_dss[0]-d_true_vs_sss[0])
    
    return d_error_array

def test_round_count_significance(num_sims, num_players=20,round_cap = 20, sss_sf=200, dss=False, shuffle=False):
    p_values_dict = {}

    if not shuffle:
        plr_list = tilted_strength(num_players)
        # random.shuffle(plr_list)
    for r in range(1,round_cap+1):
        p_values_dict[r] = []
        for i in range(num_sims):
            if shuffle:
                plr_list = tilted_strength(num_players)
                # random.shuffle(plr_list)
            else:
                for plr in plr_list:
                    plr.reset_stats()
            t = construct_tourney(plr_list)
            t.score_factor = sss_sf
            t.sim_tourney(r,double_sided=dss)
            results_list =[plr for plr in t.player_dict.values()]
            random.shuffle(results_list)
            results_list = rank_list(results_list)
            for i, player in enumerate(results_list):
                player.finish = i+1
            t_results = [plr.finish for plr in plr_list]
            
            d_true_vs_tournament = pearsonr([x for x in range(1,num_players+1)], t_results)

            p_values_dict[r].append(d_true_vs_tournament[0])
    
    return p_values_dict


def pair_looper(tourney):
    for pair in tourney.pairings:
        tourney.sim_match(pair)

if __name__ == "__main__":
    random.seed()
    # players = tilted_strength(20,0.5)
    
    # players = 32
    # num_sims = 100

    # a = collect_across_distribution(28,50,100,6,8,tilted_strength,verbose=False)
    # list_names = ['dss', '1_sss', '2_sss', '3_sss', '10_sss']
    # for item, name in zip(a,list_names):
    #     item.to_csv(f"{name}.csv")
    # tic = time()
    # score_factor = 75
    # num_rounds = 6
    # reset_counter_stats(players)
    # test_tournament_conditions(num_sims,players,num_rounds,score_factor=score_factor)
    # results_collation(players,num_sims,f"{num_sims}_sss_{num_rounds}_rnds_{len(players)}_plrs_{score_factor}_sf")
    # print((time()-tic)/60.0)

    # num_players_list = [10,16,20,28,32,40,50,60,80,100,120]
    # cap_rounds_list =  [8, 10,10,12,12,12,14,14,16,18,18]
    
    # for num_plr, rnd_cap in zip(num_players_list,cap_rounds_list):
    #     tmr = time()
    #     a = test_round_count_significance(100, round_cap= rnd_cap, num_players= num_plr, shuffle=True, dss=True)
    #     df = pd.DataFrame.from_dict(a)
    #     df.to_csv(f"{num_plr}_dss_players_corr_pearson.csv")

    #     a = test_round_count_significance(100, round_cap= rnd_cap, num_players= num_plr, shuffle=True, dss=False)
    #     df = pd.DataFrame.from_dict(a)
    #     df.to_csv(f"{num_plr}_sss_players_corr_pearson.csv")
    #     print(f"{(time()-tmr)/60}: {num_plr} with {rnd_cap}")

    players = tilted_strength(28,0.5)
    num_sims = 3000

    reset_counter_stats(players)

    test_tournament_conditions(num_tests=num_sims,player_list=players,num_rounds=8,double_sided=True)
    results_collation(players,num_sims,top_x=4,file_name= f"{3000}_dss_8_rnds_32_players")
    reset_counter_stats(players)

    score_factors = [1,2,3,10]
    for sf in score_factors:
        test_tournament_conditions(num_tests=num_sims,player_list=players,num_rounds=6,score_factor=sf)
        results_collation(players,num_sims,f"{num_sims}_sss_6_rnds_32_players_{sf}_sf",top_x=4)
        reset_counter_stats(players)