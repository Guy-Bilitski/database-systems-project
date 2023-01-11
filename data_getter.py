import requests
import re
import json
import pyodbc

HEADERS = {"accept": "application/json"}
SQL_SERVER = "localhost"
DB_NAME = "guybilitski"
DRIVER = "{SQL Server}"


def connect_to_db(uid, pwd):
    config = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}"\
        .format(DRIVER, SQL_SERVER, DB_NAME, uid, pwd)
    conn = pyodbc.connect(config, timeout=2)
    return conn.cursor()


def games_url(year):
    return 'https://api.collegefootballdata.com/games?year={}&seasonType=regular'.format(year)


def get_games(url, headers):
    res = requests.get(url, headers=headers)
    text_res = res.text
    res_list = re.split('{*}', text_res)
    res_list = list(map(lambda x: x[1:] + '}', res_list))[:-1]
    res_list = list(map(lambda x: json.loads(x), res_list))
    return res_list


def insert_games(start_year, finish_year):

    for year in range(start_year, finish_year+1):
        api_url = games_url(year)
        games = get_games(api_url, HEADERS)
        for i, doc in enumerate(games):
            pass


def main():
    with open('secret.txt') as f:
        auth = f.readline()[:-1]
        uid = f.readline()[:-1]
        pwd = f.readline()

    db = connect_to_db(uid, pwd)
    HEADERS["Authorization"] = auth
    # insert_games(1990, 2020)



if __name__ == "__main__":
    main()
