from flask import Flask, request

from bacon_backend.bacon_distance import calculate_bacon_distance
from bacon_backend.database import (
    actor_exists_by_id,
    actor_exists_by_name,
    get_100_actors,
    get_actor_id,
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


@app.get("/bacon_distance")
def request_bacon_distance():
    actor1_id = request.json["actor1_id"]
    actor2_id = request.json["actor2_id"]
    bacon_distance = calculate_bacon_distance(actor1_id, actor2_id, conn)
    return {"bacon_distance": bacon_distance}
