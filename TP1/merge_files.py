import json


def main():
    with open("./data/owned_games_raw.json", "r") as f:
        owned_games = json.load(f)
    with open("./data/owned_games_tags.json", "r") as f:
        owned_games_tags = json.load(f)

    for game in owned_games['response']['games']:
        game['tags'] = owned_games_tags[game['name']]

    json.dump(owned_games['response']['games'], open("./data/owned_games_with_tags.json", "w"), indent=2)


if __name__ == "__main__":
    main()
