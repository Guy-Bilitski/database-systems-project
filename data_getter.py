import requests


def get_games(url, headers):
    res = requests.get(url, headers=headers)
    return res


def main():
    url = "https://api.collegefootballdata.com/games?year=2020&seasonType=regular"
    headers = {"accept": "application/json"}
    with open('secret.txt') as f:
        auth = f.readline()

    headers["Authorization"] = auth
    res = get_games(url, headers)
    print(res)
    print("yes")


if __name__ == "__main__":
    main()
