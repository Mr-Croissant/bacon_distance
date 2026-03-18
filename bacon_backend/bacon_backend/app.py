from flask import Flask, request

from bacon_backend.bacon_distance import calculate_bacon_distance
from bacon_backend.database import (
    actor_exists_by_id,
    actor_exists_by_name,
    add_actor,
    add_actor_in_movie,
    add_movie,
    get_100_actors,
    get_actor_id,
    get_next_actor_id,
    get_next_movie_id,
    initialize_connection,
)

app = Flask(__name__)

conn = initialize_connection()


@app.get("/actor/exists")
def actor_exists():
    name = request.json.get("name")
    id = request.json.get("id")
    bool_actor_exists = False
    if name:
        bool_actor_exists = actor_exists_by_name(name, conn)
    elif id:
        bool_actor_exists = actor_exists_by_id(name, conn)
    return {"status": bool_actor_exists}


@app.get("/actor/id")
def return_actor_id():
    name = request.json["name"]
    actor_id = get_actor_id(name, conn)
    return {"id": actor_id}


@app.get("/actor/100")
def return_100_actors():
    first_100_actors = get_100_actors(conn)
    return {"actors": first_100_actors}

@app.post("/actor/new")
def add_new_actor():
    actor_name = request.json["name"]
    actor_id = request.json["actor_id"]
    add_actor(actor_id, actor_name, conn)
    return "", 200


@app.get("/bacon_distance")
def request_bacon_distance():
    actor1_id = request.json["actor1_id"]
    actor2_id = request.json["actor2_id"]
    bacon_distance = calculate_bacon_distance(actor1_id, actor2_id, conn)
    return {"bacon_distance": bacon_distance}


@app.post("/movie/new")
def add_new_movie():
    movie_name = request.json["name"]
    movie_id = request.json["movie_id"]
    actor_ids = request.json["actors"]
    add_movie(movie_id, movie_name, conn)
    for actor_id in actor_ids:
        add_actor_in_movie(actor_id, movie_id, conn)
    return "", 200

