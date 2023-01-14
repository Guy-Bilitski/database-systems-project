import requests
import json
import mysql.connector

HEADERS = {"accept": "application/json"}
HOST = "localhost"
DB_NAME = "guybilitski"
DRIVER = "{SQL Server}"
PORT = "3305"

VENUES_URL = "https://api.collegefootballdata.com/venues"
GAMES_URL = lambda year: 'https://api.collegefootballdata.com/games?year={}&seasonType=regular'.format(year)
TEAMS_URL = "https://api.collegefootballdata.com/teams"
RECORDS_URL = lambda year: 'https://api.collegefootballdata.com/records?year=2020'.format(year)
ATHLETES_URL = lambda year: "https://api.collegefootballdata.com/stats/player/season?year={}".format(year)
PLAYS_URL = lambda year, week: 'https://api.collegefootballdata.com/plays?seasonType=regular&year={}&week={}' \
    .format(year, week)

GAMES_INSERT_QUERY = "INSERT INTO Games" \
                     " (ID, Season, Week, Neutral_site, Venue_id, Home_id, Home_points, " \
                     " Away_id, Away_points)" \
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
VENUES_INSERT_QUERY = "INSERT INTO Venues" \
                      " (ID, Name, Capacity, Grass, City, State)" \
                      " VALUES (%s, %s, %s, %s, %s, %s)"
TEAMS_INSERT_QUERY = "INSERT INTO Teams" \
                     " (ID, School, Venue_id) VALUES (%s, %s, %s)"
RECORDS_INSERT_QUERY = "INSERT INTO Records" \
                       " (Year, Team, Expected_wins, Total_games, Wins, Losses, Ties)" \
                       " VALUES (%s, %s, %s, %s, %s, %s, %s)"
ATHLETES_INSERT_QUERY = "INSERT INTO Athletes (ID, Name) VALUES (%s, %s)"
PLAYS_INSERT_QUERY = "INSERT INTO Plays" \
                     " (ID, Team, Opponent, Distance, Athlete_id) VALUES (%s, %s, %s, %s)"


def connect_to_db(uid, pwd):
    cnx = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=uid,
        password=pwd,
        database=DB_NAME
    )
    return cnx


def convert_to_jsons(jsons_string):
    prev = 1
    count = 0
    jsons_list = []

    for i in range(1, len(jsons_string)):
        if jsons_string[i] == '{':
            count += 1
            continue
        if jsons_string[i] == '}':
            count -= 1
            if count == 0:
                new_json = json.loads(jsons_string[prev:i + 1])
                jsons_list.append(new_json)
                prev = i + 2
    return jsons_list


def get_docs(url, headers):
    res = requests.get(url, headers=headers)
    text_res = res.text
    res_list = convert_to_jsons(text_res)
    return res_list


def insert_teams(cnx):
    cursor = cnx.cursor()
    venues = get_docs(TEAMS_URL, HEADERS)
    for i, doc in enumerate(venues):
        doc_args = (doc["id"], doc["school"], doc["location"]["venue_id"])
        cursor.execute(TEAMS_INSERT_QUERY, doc_args)
        if i % 50 == 0:
            cnx.commit()
    cnx.commit()


def insert_athletes(start_year, finish_year, cnx):
    already_inserted_athletes = set()
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        athletes = get_docs(ATHLETES_URL(year), HEADERS)
        for i, doc in enumerate(athletes):
            doc_args = (doc["playerId"], doc["player"])
            if doc_args[0] in already_inserted_athletes:
                continue
            else:
                already_inserted_athletes.add(doc_args[0])
            cursor.execute(ATHLETES_INSERT_QUERY, doc_args)
            if i % 50 == 0:
                cnx.commit()
        cnx.commit()


def insert_records(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        records = get_docs(RECORDS_URL(year), HEADERS)
        for i, doc in enumerate(records):
            doc_args = (doc["year"], doc["team"], doc["expectedWins"], doc["total"]["games"], doc["total"]["wins"],
                        doc["total"]["losses"], doc["total"]["ties"])
            cursor.execute(RECORDS_INSERT_QUERY, doc_args)
            if i % 50 == 0:
                cnx.commit()
        cnx.commit()


def insert_plays(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        for week in range(1, 17):
            plays = get_docs(PLAYS_URL(year, week), HEADERS)
            for i, doc in enumerate(plays):
                doc_args = (doc["ID"], doc["Team"], doc["Opponent"], doc["Distance"], doc["Athlete_id"])
                cursor.execute(PLAYS_INSERT_QUERY, doc_args)
                if i % 50 == 0:
                    cnx.commit()
            cnx.commit()


def insert_venues(cnx):
    cursor = cnx.cursor()
    venues = get_docs(VENUES_URL, HEADERS)
    for i, doc in enumerate(venues):
        doc_args = (doc["id"], doc["name"], doc["capacity"], doc["grass"], doc["city"], doc["state"])
        cursor.execute(VENUES_INSERT_QUERY, doc_args)
        if i % 50 == 0:
            cnx.commit()
    cnx.commit()


def insert_games(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        games = get_docs(GAMES_URL(year), HEADERS)
        for i, doc in enumerate(games):
            doc_args = (doc["id"], doc["season"], doc["week"], doc["neutral_site"], doc["venue_id"],
                        doc["home_id"], doc["home_points"], doc["away_id"], doc["away_points"])
            cursor.execute(GAMES_INSERT_QUERY, doc_args)
            if i % 50 == 0:
                cnx.commit()
        cnx.commit()


def main():
    with open('secret.txt') as f:
        auth = f.readline()[:-1]
        uid = f.readline()[:-1]
        pwd = f.readline()

    HEADERS["Authorization"] = auth

    cnx = connect_to_db(uid, pwd)
    # insert_venues(cnx)
    # insert_teams(cnx)
    # insert_games(1990, 2020, cnx)
    # insert_athletes(2000, 2020, cnx)
    insert_records(1990, 2020, cnx)


if __name__ == "__main__":
    main()
