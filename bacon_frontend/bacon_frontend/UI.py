import os
from typing import Any, Dict
import requests
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

NUM_COLUMNS = 5
NUM_NAMES_PER_COLUMN = 10
SERVER_IP = "http://server:5000"
ACTOR_EXISTS_ENDPOINT = "/actor/exists"
GET_ACTOR_ID_ENDPOINT = "/actor/id"
FIRST_100_ACTORS_ENDPOINT = "/actor/100"
BACON_DISTANCE_ENDPOINT = "/bacon_distance"

print(os.environ)

def display_100_actors():
    st.divider()
    st.title("Current actors!")
    columns = st.columns(NUM_COLUMNS)
    first_100_actors = get_json_from_server(FIRST_100_ACTORS_ENDPOINT)["actors"]
    col_num = 0
    for column in columns:
        with column:
            for i in range(NUM_NAMES_PER_COLUMN):
                st.text(f"{col_num * 10 + i + 1}: {first_100_actors[col_num*10 + i][0]}")
        col_num += 1


def on_click_calculate(actor1: str, actor2: str, update_container: DeltaGenerator):
    with update_container:
        actor1_exists = get_json_from_server(ACTOR_EXISTS_ENDPOINT, {"name": actor1})["status"]
        actor2_exists = get_json_from_server(ACTOR_EXISTS_ENDPOINT, {"name": actor2})["status"]
        if actor1_exists and actor2_exists:
            actor1_id = get_json_from_server(GET_ACTOR_ID_ENDPOINT, {"name": actor1})["id"]
            actor2_id = get_json_from_server(GET_ACTOR_ID_ENDPOINT, {"name": actor2})["id"]
            bacon_distance = str(get_json_from_server(BACON_DISTANCE_ENDPOINT, {"actor1_id": actor1_id, "actor2_id": actor2_id})["bacon_distance"])
            bacon_distance = bacon_distance if bacon_distance != "-1" else "uncalculatable"
            st.badge(f"Their bacon distance is {bacon_distance}", color="green")
        else:
            st.badge("Invalid Actors", color="red", icon="🚨")


def generate_actor_picking():
    input_container = st.container()
    updates_container = st.container()
    with input_container:
        st.title("Bacon Distance 🥓🥓")
        actor1 = st.text_input("Name of first actor")
        actor2 = st.text_input("Name of second actor")
        st.button("Calculate", on_click=on_click_calculate, args=[actor1, actor2, updates_container])


def get_json_from_server(endpoint: str, data: Dict[str, Any] = {}) -> Dict[str, Any]:
    response = requests.get(SERVER_IP + endpoint, json = data)
    return response.json()

def generate_UI():
    generate_actor_picking()
    display_100_actors()


generate_UI()
