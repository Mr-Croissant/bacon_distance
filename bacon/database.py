import sqlite3
from pathlib import Path



def get_actor_name(actor_id, conn: sqlite3.Connection):
    if actor_exists(actor_id, conn):
        cur = conn.cursor()
        cur.execute("SELECT ELO FROM actors WHERE id = ?", (actor_id,))
        result = cur.fetchone()[0]
        return result
    return

def get_movie_name(movie_id, conn: sqlite3.Connection):
    if movie_exists(movie_id, conn):
        cur = conn.cursor()
        cur.execute("SELECT ELO FROM movies WHERE id = ?", (movie_id,))
        result = cur.fetchone()[0]
        return result
    return


def actor_exists(actor_id: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM actors WHERE id = ?", (actor_id,))
    result = cur.fetchone()[0]
    return result

def movie_exists(movie_id: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM movies WHERE id = ?", (movie_id,))
    result = cur.fetchone()[0]
    return result


def add_actor(actor_id: int, actor_name: str, cur: sqlite3.Cursor):
    try:
        data = (actor_id, actor_name)
        cur.execute("INSERT INTO actors VALUES(?, ?)", data)
    except Exception as e:
        print(f"An error occurred: {e}")


def add_movie(movie_id: int, movie_name: str, cur: sqlite3.Cursor):
    try:
        data = (movie_id, movie_name)
        cur.execute("INSERT INTO movies VALUES(?, ?)", data)
    except Exception as e:
        print(f"An error occurred: {e}")

def add_actor_in_movie(actor_id: int, movie_id: int, cur: sqlite3.Cursor):
    try:
        data = (actor_id, movie_id)
        cur.execute("INSERT INTO actor_to_movie VALUES(?, ?)", data)
    except Exception as e:
        print(f"An error occurred: {e}")

def initialize_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(Path(__file__).parents[1] / "bacon_distance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY,
            full_name VARCHAR(60)
        );
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            movie_name VARCHAR(60)
        );
        CREATE TABLE if not exists actor_to_movie (
            actor_id INTEGER,
            movie_id INTEGER, 
            PRIMARY KEY (actor_id, movie_id),
            FOREIGN KEY (actor_id) REFERENCES actors(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        );
        """
    )
    return conn


def reset_tables():
    conn = sqlite3.connect(Path(__file__).parents[1] / "bacon_distance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.executescript(
        """
        DROP TABLE actors;
        DROP TABLE movies;
        """
    )

conn = initialize_connection()
cursor = conn.cursor()
add_actor(1, "Ely", cursor)
add_movie(1, "Pirates of the Carribiean", cursor)
add_actor_in_movie(1, 1, cursor)