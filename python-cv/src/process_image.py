import os
from datetime import datetime
from minio import Minio
import pickle
from src.helpers.logger import get_logger
from src.helpers.ConnectionHelper import get_minio, send_to_queue, get_redis
from src.cv.detect_face import detect_face

storage = get_minio()
tasks = get_redis()
logger = get_logger(__name__)

tmp_folder = 'src/tmp'


def process_received_task(params, channel):
    task_id = str(params['task_id'])
    filename = str(params['filename'])
    logger.info("begin processing")
    logger.info(f'task_id: {task_id}, filename: {filename}')

    # get image from minio and save
    try:
        filepath = f'{tmp_folder}/{task_id}'
        storage.fget_object("images", task_id, filepath)

        # save task data to redis
        task_data = {
            'filename': filename,
            'uploaded_at': datetime.now(),
            'task_id': task_id
        }
        tasks.set(task_id, pickle.dumps(task_data))

        filename_detected = detect_face(filepath)
        # push into minio and delete local file
        storage.fput_object("images", f'{task_id}_detected', filename_detected)
        os.remove(filename_detected)

        logger.info('file saved')
        logger.info(f'task_id: {task_id}, filename: {filename_detected}')

    except Exception:
        logger.error('error receiving image', exc_info=True)
