import os
import pika
import logging.config
from src.helpers.logger import get_logger
from src.helpers.ConnectionHelper import queue_connect
from src.queue.on_channel_open import on_channel_open

logger = get_logger(__name__)


def on_connection_open(connection):
    logger.info('on_connection_open')
    connection.channel(on_open_callback=on_channel_open)


def main():
    parameters = queue_connect()

    # Подключение к очереди
    connection = pika.SelectConnection(
        parameters=parameters, on_open_callback=on_connection_open)

    # Запуск прослушивания очереди
    connection.ioloop.start()


if __name__ == "__main__":
    logger.info('started')
    main()
