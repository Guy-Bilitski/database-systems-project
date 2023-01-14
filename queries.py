

def validate_query(query):
    if not 1 <= query <= 6:
        raise Exception("there is no such query option!")


def main():
    print("Hello and welcome to college football data!")
    while True:
        print("---explain---")
        try:
            query = input("What query would you like to perform?")
            if query == "exit":
                break
            query = int(query)
            validate_query(query)
        except ValueError:
            print("Invalid input!")
            continue
        except Exception as ex:
            print(ex)
            continue


    print("Bye!")






if __name__ == "__main__":
    main()