import pika
import pika.exceptions

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


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


channel.basic_consume(queue="new_movies", on_message_callback=callback)
channel.start_consuming()