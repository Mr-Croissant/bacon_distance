import json
import random
from time import sleep

import pika
import pika.exceptions

NEW_MOVIE = "Pirates of the Carribiean"
ACTORS = ["1", "2", "3", "4", "101"]
while True:
    try:
        credentials = pika.PlainCredentials("admin", "pass")
        conn = pika.BlockingConnection(pika.ConnectionParameters(host="queue", port=5672, credentials=credentials))
        if conn:
            break
    except pika.exceptions.AMQPConnectionError:
        pass
channel = conn.channel()
channel.queue_declare(queue="new_movies")
channel.queue_declare(queue="new_actors")
channel.confirm_delivery()

def simulate_new_movie():
    channel.basic_publish(exchange='', routing_key="new_actors", body=json.dumps({"name": "Marik", "actor_id": 101}).encode())
    channel.basic_publish(
        exchange='',
        routing_key="new_movies",
        body=json.dumps({"name": NEW_MOVIE, "actors": ACTORS, "movie_id": 101}).encode(),
    )

simulate_new_movie()
