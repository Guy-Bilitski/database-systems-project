import data_getter


HEADERS = {"accept": "application/json"}
QUERY1 = "SELECT V.Name FROM Venues AS V, Players AS P, Teams AS T, Roster AS R" \
                      " WHERE %(player_name)s = P.Name" \
                      " AND P.ID = R.ID AND R.Team = T.School AND T.Venue_id = V.ID"


def validate_query(query):
    if not 1 <= query <= 6:
        raise Exception("there is no such query option!")


def pick_query(query_num, cnx):
    with cnx.cursor() as cursor:
        if query_num == 1:
            player_name = input("Insert name")
            cursor.execute(QUERY1, {'player_name': player_name})
            res = list(map(lambda x: x[0], cursor.fetchall()))
            print("Stadiums are: ", res)
        elif query_num == 2:
            pass
        elif query_num == 3:
            pass
        elif query_num == 4:
            pass
        elif query_num == 5:
            pass
        elif query_num == 6:
            pass


def main():
    with open('secret.txt') as f:
        auth = f.readline()[:-1]
        uid = f.readline()[:-1]
        pwd = f.readline()
    HEADERS["Authorization"] = auth
    cnx = data_getter.connect_to_db(uid, pwd)
    print("*** Welcome to the football college systems! we have a plenty of data for you to get to know better "
          "the league ***")
    print("You can always leave the system by typing exit")
    while True:
        print("\nOptional queries:")
        print("Option 1: Given a player's name, see all the stadiums that he played at.")
        print("Option 2: ")
        print("Option 3: ")
        print("Option 4: ")
        print("Option 5: ")
        print("Option 6: ")
        try:
            query = input("What query would you like to perform?")
            if query == "exit":
                break
            query = int(query)
            validate_query(query)
            pick_query(query, cnx)
        except ValueError:
            print("Invalid input!")
            continue
        except Exception as ex:
            print(ex)
            continue

    print("Bye!")


if __name__ == "__main__":
    main()
