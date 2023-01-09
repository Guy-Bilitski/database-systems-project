import requests
import re
import json

def get_games(url, headers):
    res = requests.get(url, headers=headers)
    return res


def main():
    url = "https://api.collegefootballdata.com/games?year=2020&seasonType=regular"
    headers = {"accept": "application/json"}
    with open('secret.txt') as f:
        auth = f.readline()

    headers["Authorization"] = auth
    text_res = get_games(url, headers).text
    res_list = re.split('{*}', text_res)
    res_list = list(map(lambda x: x[1:]+'}', res_list))[:-1]
    res_list = list(map(lambda x: json.loads(x), res_list))
    print(res_list[len(res_list) - 1])
    #for item in res_list:
    #    print(item)
    #    print(json.loads(item))
    print(text_res)


if __name__ == "__main__":
    main()
