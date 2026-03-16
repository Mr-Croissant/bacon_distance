import sqlite3

import streamlit as st
import streamlit.web.cli

from bacon.bacon_distance import calculate_bacon_distance
from bacon.database import (
    actor_exists_by_name,
    get_actor_id,
    get_all_actors,
    initialize_connection,
)

NUM_COLUMNS = 5
NUM_NAMES_PER_COLUMN = 10


def display_100_actors(conn: sqlite3.Connection):
    columns = st.columns(NUM_COLUMNS)
    first_100_actors = get_all_actors(conn)[0:100]
    col_num = 0
    for column in columns:
        with column:
            for i in range(NUM_NAMES_PER_COLUMN):
                st.text(f"{col_num * 10 + i + 1}: {first_100_actors[col_num*10 + i][0]}")
        col_num += 1


def on_click_calculate(conn: sqlite3.Connection, actor1: str, actor2: str):
    if actor_exists_by_name(actor1, conn) and actor_exists_by_name(actor2, conn):
        st.empty()
        actor1_id = get_actor_id(actor1, conn)
        actor2_id = get_actor_id(actor2, conn)
        bacon_distance = str(calculate_bacon_distance(actor1_id, actor2_id, conn))
        bacon_distance = bacon_distance if bacon_distance != "-1" else "uncalculatable"
        st.badge(f"Their bacon distance is {bacon_distance}", color="green")
    else:
        st.badge("Invalid Actors", color="red", icon="🚨")


def generate_actor_picking(conn: sqlite3.Connection):
    st.title("Bacon Distance 🥓🥓")
    actor1 = st.text_input("Name of first actor")
    actor2 = st.text_input("Name of second actor")
    st.button("Calculate", on_click=on_click_calculate, args=[conn, actor1, actor2])
    st.divider()
    st.title("Current actors!")


def generate_UI():
    conn = initialize_connection()
    generate_actor_picking(conn)
    display_100_actors(conn)


generate_UI()
