import sqlite3
from random import choice, randint
from bacon.database import (
    add_actor,
    add_actor_in_movie,
    add_movie,
    get_actor_name,
    get_actors_one_degree_away,
    get_movie_name,
    initialize_connection,
    reset_tables,
)
from bacon.random_strings import FIRST_NAMES, IDENTIFIERS, LAST_NAMES, OBJECTS

NUM_RANDOM = 1000


def generate_db() -> None:
    # reset_tables()
    conn = initialize_connection()
    # randomize_actors(conn)
    # randomize_movies(conn)
    # randomize_actors_in_movies(conn)
    add_actor(1, "Ely", conn)
    add_actor(2, "Marik", conn)
    add_actor(3, "Smith", conn)
    add_actor(4, "John", conn)
    add_movie(1, "Pirates of the Carribiean", conn)
    add_movie(2, "Pirates of the Carribiean 2", conn)
    add_actor_in_movie(1, 1, conn)
    add_actor_in_movie(2, 1, conn)
    add_actor_in_movie(3, 1, conn)
    add_actor_in_movie(1, 2, conn)
    add_actor_in_movie(4, 2, conn)
    print(get_actors_one_degree_away(1, conn))



def randomize_actors(conn: sqlite3.Connection):
    for i in range(NUM_RANDOM):
        print("Randomizing Actor: ", i)
        random_first_name = choice(FIRST_NAMES)
        random_last_name = choice(LAST_NAMES)
        add_actor(i + 1, random_first_name + " " + random_last_name, conn)

def randomize_movies(conn: sqlite3.Connection):
    for i in range(NUM_RANDOM):
        print("Randomizing Movie: ", i)
        random_identifier = choice(IDENTIFIERS)
        random_object = choice(OBJECTS)
        add_movie(i + 1, random_identifier + " of the " + random_object, conn)

def randomize_actors_in_movies(conn: sqlite3.Connection):
    for i in range(NUM_RANDOM):
        for j in range(15):
            print("Randomizing connection: ", i, " ", j)
            add_actor_in_movie(i + 1, randint(1, 1000), conn)