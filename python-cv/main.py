import os
import pika
import logging
from src.queue.on_channel_open import on_channel_open
from src.helpers.logger import get_logger

logger = get_logger(__name__)

def on_connection_open(connection):
    logger.info('on_connection_open')
    connection.channel(on_open_callback=on_channel_open)

def main():
    username = os.environ.get('QUEUE_USERNAME')
    password = os.environ.get('QUEUE_PASSWORD')
    host = os.environ.get('QUEUE_HOST')
    port = os.environ.get('QUEUE_PORT', 5672)

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

    # Подключение к очереди
    connection = pika.SelectConnection(parameters=parameters, on_open_callback=on_connection_open)

    # Запуск прослушивания очереди
    connection.ioloop.start()

if __name__ == "__main__":
    logger.info('started')
    main()