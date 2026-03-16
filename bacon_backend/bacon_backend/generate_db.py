import sqlite3
from random import choice, randint

from bacon_backend.database import (
    add_actor,
    add_actor_in_movie,
    add_movie,
    initialize_connection,
    reset_tables,
)
from bacon_backend.random_strings import FIRST_NAMES, IDENTIFIERS, LAST_NAMES, OBJECTS

NUM_RANDOM = 100


def generate_db() -> None:
    reset_tables()
    conn = initialize_connection()
    randomize_actors(conn)
    randomize_movies(conn)
    randomize_actors_in_movies(conn)


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
        for j in range(2):
            print("Randomizing connection: ", i, " ", j)
            add_actor_in_movie(i + 1, randint(1, NUM_RANDOM), conn)


generate_db()
