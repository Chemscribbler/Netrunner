from Tournament import Tournament
from Player import Player
import csv

def even_strength(player_count, round_count):
    t = Tournament()
    for _ in range(player_count):
        t.add_player(Player(str=1))
    t.sim_tournament(round_count)
    return t

def rank_results(tournament):
    tournament.player_list.sort(key= lambda player: player.sos, reverse=True)
    tournament.player_list.sort(key = lambda player: player.score, reverse=True)
    return tournament.player_list

def main():

    with open("results.csv", 'w',newline='') as csvfile:
        results_writer = csv.writer(csvfile)

        for i in range(10000):
            t = even_strength(32,4)
            ranked_players = rank_results(t)
            player_finishes = []
            for player in ranked_players:
                player_finishes.append(player.id % 32)
            results_writer.writerow(player_finishes)
            if i % 100 == 0:
                print(".")
        print("Done")


if __name__ == "__main__":
    main()