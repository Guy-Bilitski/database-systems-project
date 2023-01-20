import data_getter

HEADERS = {"accept": "application/json"}
QUERY1 = """SELECT P.Name, V.Name FROM Venues AS V, Players AS P, Teams AS T, Roster AS R
                      WHERE MATCH(P.Name) AGAINST(%(player_name)s)
                      AND P.ID = R.ID AND R.Team = T.School AND T.Venue_id = V.ID"""

QUERY2 = """SELECT t.School, mp.max_points
            FROM Teams as t, (SELECT GREATEST(apts, hpts) as max_points, tid1 as tid
	            FROM (SELECT Max(g.Away_points) as apts, t.ID as tid1
	                FROM Games as g, Teams as t
	                Where g.Away_id = t.ID GROUP BY t.ID) as max_away
	                INNER JOIN (SELECT Max(g.home_points) as hpts, t.ID as tid2
	                FROM Games as g, Teams as t
	                Where g.home_id = t.ID GROUP BY t.ID) as max_home ON max_away.tid1 = max_home.tid2
	                GROUP BY tid1) as mp
            WHERE mp.tid = t.ID"""

QUERY3 = """ SELECT v.Name as venue, vg.games as games
                FROM Venues as v, (SELECT COUNT(*) as games, g.Venue_id as vid
	                FROM Games as g
	                GROUP BY g.Venue_id) as vg
            WHERE v.ID = vg.vid
            ORDER BY games DESC"""

QUERY4 = """ SELECT beaten.team as team, COUNT(*) as years
                FROM (SELECT r.Year as year, r.Team as team
                FROM Records as r
                WHERE r.Expected_wins < r.Wins) as beaten
            GROUP BY beaten.team
            ORDER BY years DESC"""

QUERY5 = """SELECT r.Year as year, t.School as team, md.maxdiff as max_difference_wins_vs_expected
            FROM (SELECT MAX(r.Wins - r.Expected_Wins) as maxdiff, r.Year as year
                FROM Records as r
                GROUP BY r.Year) as md, Records as r, Teams as t
            WHERE r.Year = md.year AND (r.Wins - r.Expected_Wins) = md.maxdiff AND r.Team = t.School"""

QUERY6 = """ SELECT total.year as year, number_of_teams.teams_count as number_of_teams, total.games as total_games, home.games as home, away.games as away
            FROM (SELECT COUNT(*) as games, g.Season as year
                FROM Games as g
                GROUP BY g.Season) as total,
            (SELECT COUNT(*) as games, g.Season as year
                FROM Games as g
                WHERE g.home_points > g.Away_points
                GROUP BY g.Season) as home,
            (SELECT COUNT(*) as games, g.Season as year
                FROM Games as g
                WHERE g.home_points < g.Away_points
                GROUP BY g.Season) as away,
            (SELECT total.Season as year, count(*) as teams_count FROM
                (SELECT DISTINCT g.Season, g.Home_id FROM Games as g
                    UNION
                SELECT DISTINCT g.Season, g.Away_id FROM Games as g) as total
                GROUP BY total.Season) as number_of_teams
            WHERE total.year = home.year AND total.year = away.year AND total.year = number_of_teams.year
            ORDER BY year DESC"""


def validate_query(query):
    if not 1 <= query <= 6:
        raise Exception("There is no such query option!")


def pick_query(query_num, cnx):
    with cnx.cursor() as cursor:
        if query_num == 1:
            player_name = input("Insert term to search for the player's name")
            player_name = "\"" + player_name + "\""
            cursor.execute(QUERY1, {'player_name': player_name})
            res = cursor.fetchall()
            for player in res:
                print()
                print("Player: " + player[0])
                print("Stadiums of teams he played for:")
                for i in range(1, len(player)):
                    print("{}. ".format(i) + player[i])

        elif query_num == 2:
            cursor.execute(QUERY2)
            res = cursor.fetchall()
            for team in res:
                print("Team: " + team[0] + ", Max score: " + str(team[1]))

        elif query_num == 3:
            cursor.execute(QUERY3)
            res = cursor.fetchall()
            for team in res:
                print("Venue: " + team[0] + ", Number of games: " + str(team[1]))

        elif query_num == 4:
            cursor.execute(QUERY4)
            res = cursor.fetchall()
            for team in res:
                print("Team: " + team[0] + ", Number years: " + str(team[1]))

        elif query_num == 5:
            cursor.execute(QUERY5)
            res = cursor.fetchall()
            for team in res:
                print("Year: " + str(team[0]) + ", Team: " + team[1] + ", Max difference: " + str(team[2]))

        elif query_num == 6:
            cursor.execute(QUERY6)
            res = cursor.fetchall()
            for year in res:
                print("Year: " + str(year[0]) + ", Total teams: " + str(year[1]) + ", total_games: " + str(year[2])
                      + ", Home wins: " + str(year[3]) + ", Away wins: " + str(year[4]))


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
        print("Option 1: given a term, returns the stadiums of the teams that the players whose name match the term "
              "played for.")
        print("Option 2: for each team, returns the greatest amount of points it scored in a single game.")
        print("Option 3: returns the number of games played at each venue")
        print("Option 4: returns the number of years that a team had won more then expected for the coming year")
        print("Option 5: for each year returns the teams that the difference between the expected wins and actual "
              "wins is the greatest")
        print("Option 6: for each year, returns the total games played, alongside the home and away wins")
        print()
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
