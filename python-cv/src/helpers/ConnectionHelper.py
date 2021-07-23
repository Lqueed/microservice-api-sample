from minio import Minio
import os
import pika
import json
import redis


username = os.environ.get('QUEUE_USERNAME')
password = os.environ.get('QUEUE_PASSWORD')
host = os.environ.get('QUEUE_HOST', 'queue')
port = os.environ.get('QUEUE_PORT', 5672)

def get_minio():
    storage = Minio(
        'storage:9000',
        access_key=os.environ.get('MINIO_ACCESS_KEY'),
        secret_key=os.environ.get('MINIO_SECRET_KEY'),
        secure=False
    )

    found = storage.bucket_exists("images")
    if not found:
        storage.make_bucket("images")

    return storage


def send_to_queue(task_data, queue):

    parameters = pika.URLParameters(
        f'amqp://{username}:{password}@{host}:{port}/%2F')

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.exchange_declare(exchange=queue, exchange_type='fanout')
    channel.queue_bind(exchange=queue, queue=queue)
    channel.basic_publish(queue,
                          queue,
                          json.dumps(task_data))


def get_redis():
    return redis.Redis(host='redis', port=6379, db=0)


def queue_connect():
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(
        host=host,
        port=int(port),
        virtual_host='/',
        heartbeat=0,
        credentials=credentials,
        ssl_options=None,
        locale='en_US'
    )

    return parameters
