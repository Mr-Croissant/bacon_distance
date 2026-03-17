import sqlite3
from pathlib import Path
from typing import List, Optional


def get_all_actors(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT full_name FROM actors")
    result = cur.fetchall()
    return list(result)


def get_actor_id(actor_name: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id FROM actors WHERE full_name = ?", (actor_name,))
    result = cur.fetchone()
    return result[0] if result is not None else result


def get_actor_name(actor_id, conn: sqlite3.Connection):
    if actor_exists_by_id(actor_id, conn):
        cur = conn.cursor()
        cur.execute("SELECT full_name FROM actors WHERE id = ?", (actor_id,))
        result = cur.fetchone()
        return result[0] if result is not None else result
    return


def get_movie_name(movie_id, conn: sqlite3.Connection):
    if movie_exists(movie_id, conn):
        cur = conn.cursor()
        cur.execute("SELECT movie_name FROM movies WHERE id = ?", (movie_id,))
        result = cur.fetchone()
        return result[0] if result is not None else result
    return


def actor_exists_by_id(actor_id: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM actors WHERE id = ?", (actor_id,))
    result = cur.fetchone()
    return result[0] if result is not None else result


def actor_exists_by_name(actor_name: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM actors WHERE full_name = ?", (actor_name,))
    result = cur.fetchone()
    return result[0] if result is not None else result


def movie_exists(movie_id: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM movies WHERE id = ?", (movie_id,))
    result = cur.fetchone()
    return result[0] if result is not None else result


def add_actor(actor_id: int, actor_name: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    try:
        data = (actor_id, actor_name)
        cur.execute("INSERT INTO actors VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_collegues(actor_id: int, conn: sqlite3.Connection) -> Optional[List[int]]:
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT DISTINCT m2.actor_id
            FROM actor_to_movie m1
            JOIN actor_to_movie AS m2 ON m2.movie_id = m1.movie_id
            WHERE m1.actor_id = ?
            """,
            (actor_id,),
        )
        results = cur.fetchall()
        results = [result[0] for result in results]
        results = list(filter(lambda result: result != actor_id, results))
        return results
    except Exception as e:
        print(f"An error occurred: {e}")


def add_movie(movie_id: int, movie_name: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    try:
        data = (movie_id, movie_name)
        cur.execute("INSERT INTO movies VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")


def add_actor_in_movie(actor_id: int, movie_id: int, conn: sqlite3.Connection):
    cur = conn.cursor()
    try:
        data = (actor_id, movie_id)
        cur.execute("INSERT INTO actor_to_movie VALUES(?, ?)", data)
        conn.commit()
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
    conn.commit()
    return conn


def reset_tables():
    conn = sqlite3.connect(Path(__file__).parents[1] / "bacon_distance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.executescript(
        """
        DROP TABLE actors;
        DROP TABLE movies;
        DROP TABLE actor_to_movie
        """
    )
    conn.commit()
