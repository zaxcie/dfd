import tqdm
import mlbgame as mlb
import itertools
import json


def get_games_cache(year_range=range(2017, 2019), months=(3, 4, 5, 6, 7, 8, 9, 10), days=range(1, 32)):
    list_games = list()

    for year, month, day in tqdm.tqdm(itertools.product(year_range, months, days)):
        games = mlb.day(year, month, day)
        for game in games:
            list_games.append(game)
    return list_games


def games_cache_to_json(list_games):
    list_games_json = list()
    for game in list_games:
        list_games_json.append(json.loads(game.to_json()))

    return json.dumps(list_games_json)


def get_player_stats(game):
    return mlb.player_stats(game["game_id"])


def get_box_score(game):
    return mlb.box_score(game["game_id"])


if __name__ == '__main__':
    with open("/Users/kforest/workspace/dfd/data/raw/GameScoreboard_2014-2016.json", "w") as f:
        json.dump(games_cache_to_json(get_games_cache(year_range=range(2014, 2017))), f)

    with open("/Users/kforest/workspace/dfd/data/raw/GameScoreboard_2014-2016.json", "r") as f:
        cache = json.load(f)
        cache = json.loads(cache)

    print("gameScoreBoard (1/3)")

    player_stats_cache = list()
    for game in tqdm.tqdm(cache):
        try:
            player_stats_cache.append(get_player_stats(game).to_json())
        except Exception as e:
            print(game["game_id"])

    with open("/Users/kforest/workspace/dfd/data/raw/PlayerStats_2014-2016.json", "w") as f:
        json.dump(player_stats_cache, f)

    print("PlayerStats (2/3)")

    gamebox_cache = list()
    for game in tqdm.tqdm(cache):
        try:
            gamebox_cache.append(get_box_score(game).to_json())
        except Exception as e:
            print(game["game_id"])

    with open("/Users/kforest/workspace/dfd/data/raw/GameBox_2014-2016.json", "w") as f:
        json.dump(gamebox_cache, f)

    print("GameBox (3/3)")