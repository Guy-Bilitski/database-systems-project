import requests
import re
import json
import mysql.connector

HEADERS = {"accept": "application/json"}
HOST = "localhost"
DB_NAME = "guybilitski"
DRIVER = "{SQL Server}"
PORT = "3305"

VENUES_URL = "https://api.collegefootballdata.com/venues"
GAMES_URL = lambda year: 'https://api.collegefootballdata.com/games?year={}&seasonType=regular'.format(year)

GAMES_INSERT_QUERY = "INSERT INTO Games" \
                     " (ID, Season, Week, Neutral_site, Attendance, Venue_id, home_id, home_points, " \
                     "Home_post_win_prob, Away_id, Away_points, Away_post_win_prob, Excitement_index)" \
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
VENUES_INSERT_QUERY = "INSERT INTO Venues" \
                      " (ID, Name, Capacity, Grass, City, State)" \
                      " VALUES (%s, %s, %s, %s, %s, %s)"


def connect_to_db(uid, pwd):
    cnx = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=uid,
        password=pwd,
        database=DB_NAME
    )
    return cnx


def get_docs(url, headers):
    res = requests.get(url, headers=headers)
    text_res = res.text
    res_list = re.split('{*}', text_res)
    res_list = list(map(lambda x: x[1:] + '}', res_list))[:-1]
    res_list = list(map(lambda x: json.loads(x), res_list))
    return res_list


def insert_venues(cnx):
    cursor = cnx.cursor()
    venues = get_docs(VENUES_URL, HEADERS)
    for i, doc in enumerate(venues):
        doc_args = (doc["id"], doc["season"], doc["week"], doc["neutral_site"], doc["attendance"],
                    doc["venue_id"], doc["home_id"], doc["home_points"], doc["home_post_win_prob"],
                    doc["away_id"], doc["away_points"], doc["away_post_win_prob"], doc["excitement_index"])
        cursor.execute(GAMES_INSERT_QUERY, doc_args)
        if i % 50 == 0:
            cnx.commit()
    cnx.commit()


def insert_games(start_year, finish_year, cnx):
    cursor = cnx.cursor()
    for year in range(start_year, finish_year + 1):
        games = get_docs(GAMES_URL(year), HEADERS)
        for i, doc in enumerate(games):
            doc_args = (doc["id"], doc["name"], doc["capacity"], doc["grass"], doc["city"], doc["state"])
            cursor.execute(VENUES_INSERT_QUERY, doc_args)
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
    insert_venues(cnx)
    #insert_games(1990, 2020, cnx)


if __name__ == "__main__":
    main()
