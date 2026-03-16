import os
import sqlite3
from typing import Set

from bacon_backend.database import (
    actor_exists_by_name,
    get_100_actors,
    get_actor_id,
    get_collegues,
    initialize_connection,
)


def calculate_bacon_distance(start_actor_id: int, end_actor_id: int, conn: sqlite3.Connection) -> int:
    current_actors: Set[int] = set()
    current_actors.add(start_actor_id)
    visited: Set[int] = set()
    current_distance = 1
    while current_actors:
        next_degree_of_actors = get_all_collegues(current_actors, visited, conn)
        if end_actor_id in current_actors:
            return current_distance
        current_distance += 1
        current_actors = next_degree_of_actors
    return -1


def get_all_collegues(actor_ids: Set[int], visited_actors: Set[int], conn) -> Set[int]:
    distinct_collegues = set()
    for actor_id in actor_ids:
        collegues = get_collegues(actor_id, conn)
        collegues = set(collegues) if collegues is not None else set()
        distinct_collegues.update(collegues - visited_actors)
    return distinct_collegues


def get_actor_choice(conn: sqlite3.Connection) -> int:
    actor_name = ""
    conn = initialize_connection()
    while not actor_exists_by_name(actor_name, conn):
        actor_name = input("Choose Actor -> ")
        os.system("cls" if os.name == "nt" else "clear")
        print("Actor Does not exist!")
    os.system("cls" if os.name == "nt" else "clear")
    print("Excellent Choice!")
    return get_actor_id(actor_name, conn)


def get_bacon_distance_by_user_choice() -> int:
    conn = initialize_connection()
    for actor in get_100_actors(conn):
        print("Actor: ", actor[0])
    actor1 = get_actor_choice(conn)
    actor2 = get_actor_choice(conn)
    bacon_distance = calculate_bacon_distance(actor1, actor2, conn)
    return bacon_distance
