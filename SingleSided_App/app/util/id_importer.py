import requests
import os
import json

def get_all_ids(force_update=True):
    if os.path.exists("ids.json") and not force_update:
        print("Getting IDs Locally")
        all_ids = json.loads("id.json")
        return format_return(all_ids['data'])
    else:
        print("Getting ID's from Web")
        nrdb_api = "https://netrunnerdb.com/api/2.0/public"
        request = requests.get(f"{nrdb_api}/cards")
        if request.status_code != 200:
            raise Exception
        # with open('ids.json', 'w') as f:
        #     json.dump(request.json(),f)
        return format_return(request.json()['data'])    

def format_return(cards):
    corp_ids = set()
    runner_ids = set()
    for card in cards:
        if card['type_code'] == 'identity':
            if card['side_code'] == 'corp':
                corp_ids.add(card['title'])
            elif card['side_code'] == 'runner':
                runner_ids.add(card['title'])
    corp_ids = list(corp_ids)
    runner_ids = list(runner_ids)
    corp_ids.sort()
    runner_ids.sort()

    return (corp_ids, runner_ids)