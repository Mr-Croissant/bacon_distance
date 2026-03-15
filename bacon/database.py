import sqlite3
from pathlib import Path


def check_pass(username: str, password_attempt: str, conn: sqlite3.Connection):
    if user_exists(username, conn):
        cur = conn.cursor()
        cur.execute("SELECT password FROM chess_users WHERE username = ?", (username,))
        result = cur.fetchone()[0]
        return result == password_attempt
    return


def get_ELO(username, conn: sqlite3.Connection):
    if user_exists(username, conn):
        cur = conn.cursor()
        cur.execute("SELECT ELO FROM chess_users WHERE username = ?", (username,))
        result = cur.fetchone()[0]
        return int(result)
    return


def update_username(old_username: str, new_username: str, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE chess_users SET username = ? WHERE username = ?",
            (new_username, old_username),
        )
        conn.commit()
        print(f"Username updated from '{old_username}' to '{new_username}'.")
        return "Success"
    except Exception as e:
        print(f"An error occurred while updating username: {e}")
        return "Failure"


def update_password(username: str, new_password: str, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE chess_users SET password = ? WHERE username = ?",
            (new_password, username),
        )
        conn.commit()
        print(f"Password for {username} updated to '{new_password}'.")
        return "Success"
    except Exception as e:
        print(f"An error occurred while updating username: {e}")
        return "Failure"


def valid_pass(password: str):
    if password.isalnum():
        return True
    return False


def user_exists(username: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM chess_users WHERE username = ?", (username,))
    result = cur.fetchone()
    return result


def add_actor(actor_id: int, actor_name: str, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        data = (actor_id, actor_name)
        cur.execute("INSERT INTO actors VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

def add_movie(movie_id: int, movie_name: str, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        data = (movie_id, movie_name)
        cur.execute("INSERT INTO actors VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

def set_ELO(username: str, new_ELO: int, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE chess_users SET ELO = ? WHERE Username = ?", (new_ELO, username))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_top_5_players(conn: sqlite3.Connection):
    try:
        cur = conn.cursor()
        cur.execute("SELECT username, elo FROM chess_users ORDER BY elo DESC LIMIT 5")
        top_players = cur.fetchall()
        return top_players
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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

initialize_connection()

