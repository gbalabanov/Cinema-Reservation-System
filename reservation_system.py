import sqlite3
conn = sqlite3.connect("Cinema.db")
cursor = conn.cursor()


def parse_command(command):
    return tuple(command.split(" "))

def is_command(command_tuple, command_string):
    return command_tuple[0] == command_string

def verify_movie_id(arg):
    try:
        query = "Select id from movies"
        ids=[]
        for x in cursor.execute(query).fetchall():
            ids.append(x[0])
        return int(arg) in ids
    except Exception as e:
        print(e)
        return False

def get_projections_by_id(command):
    try:
        if len(command)<2:
            return ("No movie id !")
        movie_id = command[1]
        query = "Select m.name, p.date, p.time \
            From Movies as m JOIN projections as p ON m.id = p.movie_id \
            where m.id = ?"
        if not verify_movie_id(movie_id):
            return "No such movie !"
        output = cursor.execute(query,(movie_id,)).fetchall()
        for name, date, time in output:
            print("{} = {}, {}".format(name, time, date))
        return True
    except Exception as e:
        print(e)
        return False




def show_movies_func():
    try:
        output = cursor.execute("SELECT * FROM Movies ORDER BY rating DESC")
        for movie in output:
            num, name, rate = movie
            print("[{}] = {} ({})".format(num, name, rate))
        return True
    except Exception as e:
        print(e)
        return False

def show_movie_projections(args):
    return args[1]

while True:
    command = parse_command(input("Enter command--> "))

    if is_command(command,"show_movies"):
        show_movies_func()
    if is_command(command, "smp"):
        print(get_projections_by_id(command))
    if is_command(command,"exit"):
        conn.close()
        break
