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
RECORDS_URL = lambda year: 'https://api.collegefootballdata.com/records?year={}'.format(year)
PLAYERS_URL = lambda year: "https://api.collegefootballdata.com/roster?year={}".format(year)
ROSTER_URL = lambda year: "https://api.collegefootballdata.com/roster?year={}".format(year)

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
PLAYERS_INSERT_QUERY = "INSERT INTO Players (ID, Name) VALUES (%s, %s)"
ROSTER_INSERT_QUERY = "INSERT INTO Roster" \
                      " (ID, Team, Year) VALUES (%s, %s, %s)"


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
    """ Converts a long string that represents a list of valid jsons into a real python list of dictionaries """
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
    """ The function that returns the list of jsons received from the API """
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
    cnx.commit()


def insert_players(start_year, finish_year, cnx):
    already_inserted_players = set()
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        players = get_docs(PLAYERS_URL(year), HEADERS)
        for i, doc in enumerate(players):
            try:
                doc_args = (doc["id"], doc["first_name"] + " " + doc["last_name"])
                if doc_args[1] == '- Team':
                    continue
            except Exception:
                continue
            if doc_args[0] in already_inserted_players:
                continue
            else:
                already_inserted_players.add(doc_args[0])
            cursor.execute(PLAYERS_INSERT_QUERY, doc_args)
        cnx.commit()


def insert_records(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        records = get_docs(RECORDS_URL(year), HEADERS)
        for i, doc in enumerate(records):
            doc_args = (doc["year"], doc["team"], doc["expectedWins"], doc["total"]["games"], doc["total"]["wins"],
                        doc["total"]["losses"], doc["total"]["ties"])
            cursor.execute(RECORDS_INSERT_QUERY, doc_args)
        cnx.commit()


def insert_roster(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    already_inserted_players = set()
    for year in range(start_year, finish_year + 1):
        roster = get_docs(ROSTER_URL(year), HEADERS)
        for i, doc in enumerate(roster):
            try:
                if doc["first_name"] + " " + doc["last_name"] == '- Team':
                    continue
                doc_args = (doc["id"], doc["team"], year)
            except Exception:
                continue
            if doc_args[0] in already_inserted_players:
                continue
            else:
                already_inserted_players.add(doc_args[0])
            cursor.execute(ROSTER_INSERT_QUERY, doc_args)
        cnx.commit()


def insert_venues(cnx):
    cursor = cnx.cursor()
    venues = get_docs(VENUES_URL, HEADERS)
    for i, doc in enumerate(venues):
        doc_args = (doc["id"], doc["name"], doc["capacity"], doc["grass"], doc["city"], doc["state"])
        cursor.execute(VENUES_INSERT_QUERY, doc_args)
    cnx.commit()


def insert_games(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        games = get_docs(GAMES_URL(year), HEADERS)
        for i, doc in enumerate(games):
            doc_args = (doc["id"], doc["season"], doc["week"], doc["neutral_site"], doc["venue_id"],
                        doc["home_id"], doc["home_points"], doc["away_id"], doc["away_points"])
            cursor.execute(GAMES_INSERT_QUERY, doc_args)
        cnx.commit()


def main():
    # Reads the secrets (password, user id). This file should never be uploaded the web (e.g github, bitbucket, etc)
    with open('../DOCUMENTATION/MYSQL-USER-AND-PASSWORD.txt') as f:
        auth = f.readline()[:-1]
        uid = f.readline()[:-1]
        pwd = f.readline()

    HEADERS["Authorization"] = auth

    # insert_x is responsible for the insertion of all data to the DB
    # The order is crucial due to foreign key dependence
    # This script should run only once after building the DB using CREATE-DB-SCRIPT.sql
    cnx = connect_to_db(uid, pwd)
    insert_venues(cnx)
    insert_teams(cnx)
    insert_games(1990, 2020, cnx)
    insert_records(1990, 2020, cnx)
    insert_players(2013, 2020, cnx)
    insert_roster(2013, 2020, cnx)


if __name__ == "__main__":
    main()
