import json
from tkinter import filedialog

min_play_cutoff = 1
filename = filedialog.askopenfilename(title="Select .json for import")
f = open(filename, encoding='utf8')
cobrai_data = json.load(f)

results_file_path = filedialog.asksaveasfilename(title="Save Results",filetypes = (("Text File",".txt"),),defaultextension = ".txt")

runnerScore = 0
corpScore = 0


with open(results_file_path,"w") as results_file:
    for data_round in cobrai_data["rounds"]:
        for table in data_round:
            if not table["eliminationGame"]:
                try:
                    runnerScore += table["player1"]["runnerScore"]
                    runnerScore += table["player2"]["runnerScore"]
                    corpScore += table["player1"]["corpScore"]
                    corpScore += table["player2"]["corpScore"]
                except TypeError as e:
                    pass
            else:
                if table['player1']['role'] == "corp":
                    if table['player1']['winner']:
                        corpScore += 3
                    else:
                        runnerScore += 3
                else:
                    if table['player1']['winner']:
                        runnerScore += 3
                    else:
                        corpScore += 3                          

    results_file.write(f"Runner Wins: {runnerScore/3} {runnerScore/(runnerScore+corpScore) * 100}% \tCorp Wins: {corpScore/3} {corpScore/(runnerScore+corpScore) * 100}%\n")


    Corp_ID_Dict = {}
    Runner_ID_Dict = {}

    for player in cobrai_data['players']:
        try:
            Corp_ID_Dict[player["corpIdentity"]][player["id"]] = {"Wins":0,"Losses":0}
        except KeyError as identifier:
            Corp_ID_Dict[player["corpIdentity"]] = {}
            Corp_ID_Dict[player["corpIdentity"]][player["id"]] = {"Wins":0,"Losses":0}
        try:
            Runner_ID_Dict[player["runnerIdentity"]][player["id"]] = {"Wins":0,"Losses":0}
        except KeyError as identifier:
            Runner_ID_Dict[player["runnerIdentity"]] = {}
            Runner_ID_Dict[player["runnerIdentity"]][player["id"]] = {"Wins":0,"Losses":0}

    for play_round in cobrai_data["rounds"]:
        for table in play_round:
            for corp, players in Corp_ID_Dict.items():
                try:
                    if table["player1"]["corpScore"] > 0:
                        players[table["player1"]["id"]]["Wins"] += 1
                    else:
                        players[table["player1"]["id"]]["Losses"] += 1
                except KeyError as identifier:
                    pass
                except TypeError:
                    pass
                try:
                    if table["player2"]["corpScore"] > 0:
                        players[table["player2"]["id"]]["Wins"] += 1
                    else:
                        players[table["player2"]["id"]]["Losses"] += 1
                except KeyError as identifier:
                    pass
                except TypeError:
                    pass
            for runner, players in Runner_ID_Dict.items():
                try:
                    if table["player1"]["runnerScore"] > 0:
                        players[table["player1"]["id"]]["Wins"] += 1
                    else:
                        players[table["player1"]["id"]]["Losses"] += 1
                except KeyError as identifier:
                    pass
                except TypeError:
                    pass
                try:
                    if table["player2"]["runnerScore"] > 0:
                        players[table["player2"]["id"]]["Wins"] += 1
                    else:
                        players[table["player2"]["id"]]["Losses"] += 1
                except KeyError as identifier:
                    pass
                except TypeError:
                    pass

    for runner_id, player_results in Runner_ID_Dict.items():
        wins = 0
        losses = 0
        for player in player_results.values():
            wins += player["Wins"]
            losses += player["Losses"]
        Runner_ID_Dict[runner_id]["wins"] = wins
        Runner_ID_Dict[runner_id]["losses"] = losses

    for corp_id, player_results in Corp_ID_Dict.items():
        wins = 0
        losses = 0
        for player in player_results.values():
            wins += player["Wins"]
            losses += player["Losses"]
        Corp_ID_Dict[corp_id]["wins"] = wins
        Corp_ID_Dict[corp_id]["losses"] = losses




    for runner_id in sorted(Runner_ID_Dict, key= lambda x: (Runner_ID_Dict[x]['wins']), reverse=True):
        wins = Runner_ID_Dict[runner_id]['wins']
        losses = Runner_ID_Dict[runner_id]['losses']
        win_percent = round((wins/(wins+losses))*100,0)
        if(wins + losses > min_play_cutoff):
            results_file.write(f"{runner_id}:\t{wins}:{losses}\t{win_percent}%\n")
    for corp_id in sorted(Corp_ID_Dict, key= lambda x: (Corp_ID_Dict[x]['wins']), reverse=True):
        wins = Corp_ID_Dict[corp_id]['wins']
        losses = Corp_ID_Dict[corp_id]['losses']
        win_percent = round((wins/(wins+losses))*100,0)
        if(wins + losses > min_play_cutoff):
            results_file.write(f"{corp_id}:\t{wins}:{losses}\t{win_percent}%\n")




# for runner_id in sorted(Runner_ID_Dict, key= lambda x: (Runner_ID_Dict[x]['wins']), reverse=True):
#     wins = Runner_ID_Dict[runner_id]['wins']
#     losses = Runner_ID_Dict[runner_id]['losses']
#     win_percent = round((wins/(wins+losses))*100,0)
#     if(wins + losses > min_play_cutoff):
#         print(f"{runner_id}:\t{wins}:{losses}\t{win_percent}%")

# for corp_id in sorted(Corp_ID_Dict, key= lambda x: (Corp_ID_Dict[x]['wins']), reverse=True):
#     wins = Corp_ID_Dict[corp_id]['wins']
#     losses = Corp_ID_Dict[corp_id]['losses']
#     win_percent = round((wins/(wins+losses))*100,0)
#     if(wins + losses > min_play_cutoff):
#         print(f"{corp_id}:\t{wins}:{losses}\t{win_percent}%")

