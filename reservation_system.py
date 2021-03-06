import sqlite3
conn = sqlite3.connect("Cinema.db")
cursor = conn.cursor()


def print_room_seats(room):
    for row in room:
        print(" | ".join(row))


def get_projection_seats_as_tuples(proj_id):
    query = """  Select r.row, r.col
                From reservations as r
                join projections as p
                on r.projection_id = p.id
                where p.id = ?"""
    seats = cursor.execute(query, (proj_id, )).fetchall()
    return seats


def get_free_seats_for_projection(proj_id):
    query = """Select 100 - count(r.id)
                from projections as p
                left join reservations as r on p.id = r.projection_id
                where p.id = ?"""
    output = cursor.execute(query, (proj_id,)).fetchone()
    return output[0]


def make_reservation():
    room_seats = [["." for x in range(10)] for y in range(10)]
    user_seats = []
    try:
        name = input("Enter name-->")
        number_tickets = int(input("Enter number of tickets-->"))
        show_movies_func()
        movie_id = input("Enter movie id--> ")
        while not (movie_id == "cancel" or verify_movie_id(movie_id)):
            movie_id = input("Enter correct id--> ")
        get_projections_by_movie_id(movie_id)
        proj_id = input("Choose a projection--> ")
        if number_tickets > get_free_seats_for_projection(proj_id):
            print(
                "There are no {} free seats for that projection !".format(number_tickets))
            return False
        for seat in get_projection_seats_as_tuples(proj_id):
            room_seats[seat[0] - 1][seat[1] - 1] = "X"
        print_room_seats(room_seats)
        for x in range(number_tickets):
            seat = eval(input("Enter seat--> "))
            row, col = seat
            while seat in get_projection_seats_as_tuples(proj_id) or (row > 10 or col > 10) or seat in user_seats:
                print("Invalid seat !")
                seat = eval(input("Enter another seat--> "))
                row, col = seat
            user_seats.append(seat)


    except Exception as e:
        print(e)
        return False


def parse_command(command):
    return tuple(command.split(" "))


def is_command(command_tuple, command_string):
    return command_tuple[0] == command_string


def verify_movie_id(arg):
    if arg == "cancel":
        return False
    try:
        query = "Select id from movies"
        ids = []
        for x in cursor.execute(query).fetchall():
            ids.append(x[0])
        return int(arg) in ids
    except Exception as e:
        print(e)
        return False


def get_projections_by_projection_id(projection_id):
    try:
        pass

    except Exception as e:
        print(e)
        return False


def get_projections_by_movie_id(movie_id):
    try:
        # if len(command) < 2:
        #    return ("No movie id !")
        #movie_id = command
        query = """select p.id, 100-count(r.id) as free_spaces, m.name, p.date, p.time
                    from projections as p left join reservations as r
                    on r.projection_id = p.id
                    join movies as m on p.movie_id = m.id
                    where m.id = ?
                    group by(r.projection_id) """
        if not verify_movie_id(movie_id):
            return "No such movie !"
        output = cursor.execute(query, (movie_id,)).fetchall()
        for x in output:
            p_id, count, name, date, time = x
            print(
                "({}) {} - {}, {}, {} free spaces".format(p_id, name, date, time, count))
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


while True:
    command = parse_command(input("Enter command--> "))

    if is_command(command, "show_movies"):
        show_movies_func()
    if is_command(command, "smp"):
        if len(command) > 1:
            print(get_projections_by_movie_id(command[1]))
    if is_command(command, "mr"):
        make_reservation()
    if is_command(command, "exit"):
        conn.close()
        break
