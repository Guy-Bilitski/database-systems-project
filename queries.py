

def validate_query(query):
    if 1 > query > 6:
        raise Exception("there is no such query option!")


def main():
    print("Hello and welcome to college football data!")
    while True:
        print("---explain---")
        try:
            query = int(input("What query would you like to perform?"))
            validate_query(query)
        except ValueError:
            print("Invalid input!")
        except Exception as ex:
            print(ex)
        finally:
            continue




if __name__ == "__main__":
    main()