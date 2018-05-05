import datetime
import tqdm
import mlbgame as mlb
import itertools
import json
import pandas as pd
import numpy as np


def get_games_cache(year_range=range(2017, 2019), months=(3, 4, 5, 6, 7, 8, 9, 10), days=range(1, 32)):
    list_games = list()

    for year, month, day in tqdm.tqdm(itertools.product(year_range, months, days)):
        games = mlb.day(year, month, day)
        for game in games:
            list_games.append(game)
        print(month)
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
    # with open("/Users/kforest/workspace/dfd/data/raw/GameScoreboard_2018-04-23.json", "w") as f:
    #    json.dump(games_cache_to_json(get_games_cache(year_range=range(2017, 2019))), f)

    with open("/Users/kforest/workspace/dfd/data/raw/GameScoreboard_2018-04-23.json", "r") as f:
        cache = json.load(f)
        cache = json.loads(cache)

    # player_stats_cache = list()
    # for game in tqdm.tqdm(cache):
    #     try:
    #         player_stats_cache.append(get_player_stats(game).to_json())
    #     except Exception as e:
    #         print(game["game_id"])

    gamebox_cache = list()
    for game in tqdm.tqdm(cache):
        try:
            gamebox_cache.append(get_box_score(game).to_json())
        except Exception as e:
            print(game["game_id"])

    with open("/Users/kforest/workspace/dfd/data/raw/GameBox_2018-04-29.json", "w") as f:
        json.dump(gamebox_cache, f)
