import data_getter


HEADERS = {"accept": "application/json"}
QUERY1 = lambda name: "SELECT V.Name" \
                      " FROM Venues AS V, Players AS P, Teams AS T, Roster AS R" \
                      " WHERE {} = P.Name" \
                      " AND P.ID = R.ID AND R.Team = T.School AND T.Venue_id = V.ID".format(name)

def validate_query(query):
    if not 1 <= query <= 6:
        raise Exception("there is no such query option!")


def pick_query(query_num, cnx):
    cursor = cnx.cursor()
    if query_num == 1:
        name = input("Insert name")
        cursor.execute(QUERY1(name))
        res = cursor.fetchall()
        print("Stadiums are: ", res)


def main():
    with open('secret.txt') as f:
        auth = f.readline()[:-1]
        uid = f.readline()[:-1]
        pwd = f.readline()
    HEADERS["Authorization"] = auth
    cnx = data_getter.connect_to_db(uid, pwd)
    print("Hello and welcome to college football data!")
    while True:
        print("---explain---")
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
