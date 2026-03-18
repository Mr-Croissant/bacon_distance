import json

import pika
import pika.exceptions
import requests

NEW_MOVIE_ENDPOINT = "/movie/new"
NEW_ACTOR_ENDPOINT = "/actor/new"

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
channel.queue_declare(queue="new_actors")
channel.confirm_delivery()


def send_update_to_server(ch, method, properties, body, endpoint):
    print("New message from queue: ", body)
    response = requests.post("http://server:5000/" + endpoint, json=json.loads(body.decode()))
    if response.status_code == 200:
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="new_movies", on_message_callback=send_update_to_server, arguments={"endpoint": NEW_MOVIE_ENDPOINT})
channel.basic_consume(queue="new_actors", on_message_callback=send_update_to_server, arguments={"endpoint": NEW_ACTOR_ENDPOINT})
print("Started Consuming!")
channel.start_consuming()
