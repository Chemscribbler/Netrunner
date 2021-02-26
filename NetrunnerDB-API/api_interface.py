import requests
import csv
import json

root_address = "https://netrunnerdb.com/api/2.0/"

# For pulling from next rotation (AKA Mumbad-Gateway)
valid_codes = [
    "sansan",
    "honor-and-profit",
    "order-and-chaos",
    "data-and-destiny",
    "mumbad",
    "flashpoint",
    "red-sand",
    "kitara",
    "reign-and-reverie",
    "magnum-opus",
    "ashes",
    "sc19",
]

# Requesting all cards, then filtering on valid codes. Will add each card name, side, and faction to a dictionary

# response = requests.get(root_address+"public/cards")

# with open("cards.json",'w',newline='') as jsonfile:
#     json.dump(response.json(),jsonfile)

# response = requests.get(root_address+"public/packs")

# with open("packs.json",'w',newline='') as jsonfile:
#     json.dump(response.json(),jsonfile)

with open("packs.json") as f:
    all_packs = json.load(f)

filtered_packs = []

for pack in all_packs["data"]:
    if pack["cycle_code"] in valid_codes:
        filtered_packs.append(pack["code"])

with open("cards.json") as f:
    all_cards = json.load(f)

legal_cards = {}

for card in all_cards["data"]:
    if card["pack_code"] in filtered_packs:
        legal_cards[card["title"]] = {
            "faction": card["faction_code"],
            "card_type": card["type_code"],
        }

with open("legal_cards.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for key, value in legal_cards.items():
        w.writerow([key, value["faction"], value["card_type"]])
