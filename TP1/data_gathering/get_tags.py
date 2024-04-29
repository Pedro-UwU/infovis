import html_to_json as htj
import requests
import json
from pprint import pprint
from multiprocessing.pool import ThreadPool


def main():
    with open("./data/owned_games_raw.json", "r") as f:
        owned_games = json.load(f)

    games = dict()
    thread_pool = ThreadPool(8)
    # games = thread_pool.map(get_tags, [game['appid'] for game in owned_games['response']['games']])

    # Map to games with format { "name": [tags] }
    games = thread_pool.map(lambda x: {x['name']: get_tags(x['appid'])}, owned_games['response']['games'])
    pprint(games)
    json.dump(games, open("./data/owned_games_tags.json", "w"), indent=2)

    # html = requests.get("https://store.steampowered.com/app/1245620").text
    # get_tags("1245620")


def get_tags(id: str) -> list:
    html = requests.get(f"https://store.steampowered.com/app/{id}").text
    json_str = json.dumps(htj.convert(html), indent=2)
    # For each line, if the string "app_tag" is in there, print the 3 line surrowning it
    tags = list()
    for i, line in enumerate(json_str.split("\n")):
        if '"app_tag"' in line:
            line_to_save = i
            while "_value" not in json_str.split("\n")[line_to_save]:
                line_to_save += 1
            value = json_str.split("\n")[line_to_save].strip()
            value = value.split(":")
            if len(value) > 0:
                value = value[-1].strip().replace('"', "")
            else:
                print(f"Error in id {id}")
                continue
            if value != "" and value != "+":
                tags.append(value)
    return tags


if __name__ == "__main__":
    main()
