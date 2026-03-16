import os
import sqlite3
from typing import Set

from bacon.database import (
    actor_exists_by_name,
    get_actor_id,
    get_all_actors,
    get_collegues,
    initialize_connection,
)

MAX_DISTANCE = 5


def _calculate_bacon_distance(start_actor_id: int, end_actor_id: int, conn: sqlite3.Connection) -> int:
    current_actors: Set[int] = set()
    current_actors.add(start_actor_id)
    for current_distance in range(MAX_DISTANCE):
        current_actors = get_all_collegues(current_actors, conn)
        if end_actor_id in current_actors:
            return current_distance + 1
    return -1


def get_all_collegues(actor_ids: Set[int], conn) -> Set[int]:
    distinct_collegues = set()
    for actor_id in actor_ids:
        collegues = get_collegues(actor_id, conn)
        distinct_collegues.update(collegues)
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
    for actor in get_all_actors(conn):
        print("Actor: ", actor[0])
    actor1 = get_actor_choice(conn)
    actor2 = get_actor_choice(conn)
    bacon_distance = _calculate_bacon_distance(actor1, actor2, conn)
    return bacon_distance
