
import logging

console_template = '%(levelname)s: %(message)s,"service":"api","timestamp":"%(asctime)s"'
log_template = '{"message":"%(message)s","level":"%(levelname)s","service":"api","timestamp":"%(asctime)s"}'

logname = 'log/combined.log'

error_handler = logging.FileHandler("log/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(log_template))

base_handler = logging.FileHandler("log/combined.log")
base_handler.setLevel(logging.INFO)
base_handler.setFormatter(logging.Formatter(log_template))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(console_template))

logging.basicConfig(
  format='{"message":"%(message)s","level":"%(levelname)s","service":"api","timestamp":"%(asctime)s"}',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      error_handler,
      base_handler,
      stream_handler
  ]
)

def get_logger(name):
  logger = logging.getLogger(name)
  return logger

