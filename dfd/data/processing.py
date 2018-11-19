import pandas as pd
import numpy as np
from dfd.config import MLBGAME_DB
import sqlalchemy as alch

#
# engine = alch.create_engine('postgresql://postgres:admin@localhost:5432/mlbgames')
# query = "SELECT * FROM pitching"
# pitching = pd.read_sql_query(query, engine)
#
# query = "SELECT batting.*, gamescore.date FROM batting INNER JOIN gamescore ON batting.game_id=gamescore.game_id"
#
# batting = pd.read_sql_query(query, engine)


def get_gamescore(db_url=None):
    if db_url is None:
        engine = alch.create_engine(MLBGAME_DB)

    else:
        engine = alch.create_engine(db_url)

    query = "SELECT * FROM gamescore"

    gamescore = pd.read_sql_query(query, engine)
    gamescore = gamescore_process(gamescore)

    return gamescore


def gamescore_process(gamescore):
    gamescore["date"] = pd.to_datetime(gamescore["date"])

    for team in gamescore["home_team"].unique():
        is_home = gamescore["home_team"] == team
        is_away = gamescore["away_team"] == team
        print(gamescore[is_home | is_away].sort_values(by=["date"])["game_id"])

        print(gamescore["date"].dt.year)
    return gamescore


def get_batting(db_url=None):
    if db_url is None:
        engine = alch.create_engine(MLBGAME_DB)

    else:
        engine = alch.create_engine(db_url)

    query = "SELECT batting.*, gamescore.date FROM batting INNER JOIN gamescore ON batting.game_id=gamescore.game_id"

    batting = pd.read_sql_query(query, engine)
    batting["date"] = pd.to_datetime(batting["date"])

    return batting


if __name__ == '__main__':
    gamescore = get_gamescore()
