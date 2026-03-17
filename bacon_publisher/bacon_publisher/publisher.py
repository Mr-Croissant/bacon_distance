import json
import random
from time import sleep

import pika
import pika.exceptions

NEW_MOVIES = ["Pirates of the Carribiean", "New Boys", "Girl on the Block"]
ACTORS = ["Marik", "Ely", "Or", "Yoni", "Michal"]
while True:
    try:
        credentials = pika.PlainCredentials("admin", "pass")
        conn = pika.BlockingConnection(pika.ConnectionParameters(host="queue", credentials=credentials))
        if conn:
            break
    except pika.exceptions.AMQPConnectionError:
        pass
channel = conn.channel()
channel.queue_declare(queue="new_movies")


def simulate_new_movies():
    print("publishing!!")
    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body=json.dumps({"name": random.choice(NEW_MOVIES), "actors": ACTORS}).encode(),
        mandatory=True
    )
    print("apparnetly publishedf but in reality who knows")


print("testing")

while True:
    simulate_new_movies()
    sleep(100)
