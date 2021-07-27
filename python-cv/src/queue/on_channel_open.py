import pika
import traceback
import json
from src.process_image import process_received_task
from src.helpers.logger import get_logger

logger = get_logger(__name__)

def on_channel_open(channel):
    logger.info('on_channel_open')
    channel.queue_declare('task_queue')
    channel.basic_consume(on_message_callback=channel_callback, queue='task_queue')

def channel_callback(ch, method, props, body):
    logger.info('channel_callback')

    requestData = json.loads(body)
    process_received_task(requestData, ch)
    
    ch.basic_ack(method.delivery_tag)
