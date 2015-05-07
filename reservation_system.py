import sqlite3
conn = sqlite3.connect("Cinema.db")
cursor = conn.cursor()


def parse_command(command):
    return tuple(command.split(" "))

def is_command(command_tuple, command_string):
    return command_tuple[0] == command_string

def show_movies_func():
    try:
        output = cursor.execute("Select * from Movies")
        for movie in output:
            num, name, rate = movie
            print("[{}] = {} ({})".format(num, name, rate))
        return True
    except Exception as e:
        print(e)
        return False


while True:
    command = parse_command(input("Enter command--> "))

    if is_command(command,"show_movies"):
        show_movies_func()
