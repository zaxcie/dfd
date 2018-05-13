import csv
import sqlite3
import os
import json
import psycopg2
import copy


def format_col_for_create_table(cols):
    col_names = "(" + cols[0]
    value_names = "(?"

    for i in range(1, len(cols)):
        col_names += ", " + cols[i]
        value_names += ", ?"

    col_names += ")"
    value_names += ")"

    return col_names, value_names


def create_lahman_db(db_path, csv_path):
    con = sqlite3.connect(db_path)

    for csv_file in os.listdir(csv_path):
        file_path = csv_path + csv_file

        with open(file_path, 'r') as f:
            dr = csv.DictReader(f)

            to_db = list()

            for row in dr:
                record = list()
                for col in dr.fieldnames:
                    record.append(row[col])

                to_db.append(tuple(record))

        format_cols, format_values = format_col_for_create_table(dr.fieldnames)
        cur = con.cursor()
        cur.execute("CREATE TABLE " + csv_file.split(".")[0] + " " + format_cols + ";")

        cur.executemany("INSERT INTO " + csv_file.split(".")[0] + " " + format_cols + " VALUES " +
                        format_values + ";", to_db)
        con.commit()

    con.close()


def create_game_db(db_path, gamescore_path, player_stat_path, gamnebox_path):
    with open(gamescore_path, "r") as f:
        gamescores = json.load(f)

    with open(gamnebox_path, "r") as f:
        gamebox = json.load(f)

    with open(player_stat_path, "r") as f:
        playerstats = json.load(f)
        _playerstats = list()
        for i in playerstats:
            _playerstats.append(json.loads(i))

        playerstats = _playerstats


    con = sqlite3.connect(db_path)
    create_gamescore_table(con, gamescores)
    # for gamestat_cat in ["home_pitching", "away_pitching", "home_batting", "away_batting",
    #                      "home_additional_pitching", "away_additional_pitching",
    #                      "home_additional_batting", "away_additional_batting"]:
    #     create_player_stats_table(con, playerstats, gamestat_cat, gamestat_cat)

    create_inning_table(con, gamebox)
    con.close()


def create_dictkey_set(l):
    key_set = set()

    for d in l:
        for key in d:
            key_set.add(key)

    return key_set


def create_gamescore_table(con, gamescores):
    cur = con.cursor()
    cols = create_dictkey_set(gamescores)
    format_cols, format_values = format_col_for_create_table(list(cols))
    cur.execute('DROP TABLE if EXISTS GameScore')

    cur.execute("CREATE TABLE GameScore " + format_cols + ";")

    for i in gamescores:
        value_list = list()
        for key in cols:
            value_list.append(i.get(key, None))

        cur.execute("INSERT INTO GameScore VALUES " + format_values, value_list)

    con.commit()


def create_inning_table(con, gamebox):
    cur = con.cursor()

    gamebox_obj = list()

    for i in gamebox:
        gamebox_obj.append(json.loads(i))
    gamebox = gamebox_obj

    expand_gamebox = list()

    for game in gamebox:
        max_inning = int(game["innings"][0]["inning"])
        final_inning = copy.copy(game["innings"][0])
        final_inning["inning"] = "Final"

        for inning in game["innings"]:
            expand_inning = dict()
            expand_inning['game_id'] = game["game_id"]
            expand_inning["inning"] = int(inning["inning"])
            expand_inning["home"] = inning["home"]
            expand_inning["away"] = inning["away"]
            expand_gamebox.append(expand_inning)

    cols = create_dictkey_set(expand_gamebox)

    format_cols, format_values = format_col_for_create_table(list(cols))
    cur.execute('DROP TABLE if EXISTS GameBox')

    cur.execute("CREATE TABLE GameBox " + format_cols + ";")

    for i in gamebox:
        value_list = list()
        for key in cols:
            value_list.append(i.get(key, None))

        cur.execute("INSERT INTO GameBox VALUES " + format_values, value_list)

    con.commit()


def create_player_stats_table(con, gamestat, gamestat_cat, table_name):
    cur = con.cursor()
    player_names = set()

    for game in gamestat:
        for i in game[gamestat_cat]:
            player_names.add(i["name_display_first_last"])

    stats_keys = set()
    for game in gamestat:
        stats_keys = stats_keys.union(create_dictkey_set(list(game[gamestat_cat])))

    cols = list(stats_keys)
    cols.append("game_id")
    format_cols, format_values = format_col_for_create_table(cols)

    cur.execute('DROP TABLE if EXISTS ' + table_name)

    cur.execute("CREATE TABLE " + table_name + " " + format_cols + ";")

    for game in gamestat:
        for i in game[gamestat_cat]:
            value_list = list()
            for key in stats_keys:
                value_list.append(i.get(key, None))
            value_list.append(game["game_id"])

            cur.execute("INSERT INTO " + table_name + " VALUES " + format_values, value_list)

    con.commit()


if __name__ == '__main__':
    create_game_db("data/processed/mlbgame.sqlite",
                   "data/processed/score.json",
                   "data/processed/player.json",
                   "data/processed/gamebox.json")

    # create_lahman_db("/Users/kforest/workspace/dfd/data/processed/lahman-2017.sqlite",
    #                  "/Users/kforest/workspace/dfd/data/raw/baseballdatabank-master/core/")
