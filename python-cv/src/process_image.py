import redis
from src.helpers.logger import get_logger

logger = get_logger(__name__)

def process_received_task(params, channel):
  task_id = str(params['task_id'])
  filename = str(params['filename'])
  logger.info("begin processing")
  print('i am working')
  print(params)
  db = redis.Redis(host='redis', port=6379, db=0)
  db.set('test_key', 'test_value')
  db.set(task_id, filename)