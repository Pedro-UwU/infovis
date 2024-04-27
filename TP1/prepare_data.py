import json
from pprint import pprint

def main():
    print("Hello World!")
    with open('./data/owned_games_raw.json', 'r') as f:
        games = json.load(f)['response']['games']

    with open('./data/owned_games_tags.json', 'r') as f:
        tags = json.load(f)
    data = dict()

    for game in games:
        game_data = dict()
        name = game['name']
        game_data['tags'] = tags[name] if name in tags else []
        total_win = game['playtime_windows_forever'] if 'playtime_windows_forever' in game else 0
        total_linux = game['playtime_linux_forever'] if 'playtime_linux_forever' in game else 0
        total_mac = game['playtime_mac_forever'] if 'playtime_mac_forever' in game else 0
        game_data['total_win'] = total_win
        game_data['total_linux'] = total_linux
        game_data['total_mac'] = total_mac
        data[name] = game_data

    tag_list = get_all_tags(tags)
    pprint(tag_list)

    headers = ['name', 'total_win', 'total_linux', 'total_mac'] + tag_list
    pprint(headers)
    lines = [headers]
    for game, game_data in data.items():
        line = [f'"{game}"', game_data['total_win'], game_data['total_linux'], game_data['total_mac']]
        for tag in tag_list:
            line.append(1 if tag in game_data['tags'] else 0)
        lines.append(line)

    with open("./data/data.csv", 'w') as f:
        for line in lines:
            f.write(','.join(map(str, line)) + '\n')



def get_all_tags(tags) -> list:
    all_tags = []
    for game, game_tags in tags.items():
        for tag in game_tags:
            if tag not in all_tags:
                all_tags.append(tag)
    return all_tags


if __name__ == "__main__":
    main()
