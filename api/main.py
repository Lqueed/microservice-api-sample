from flask import Flask, render_template, request
from flask import send_file
import logging
from helpers.logger import get_logger
from helpers.ConnectionHelper import get_minio, send_to_queue
import os
import uuid
import json

logger = get_logger(__name__)
app = Flask(__name__)

MAX_FILE_SIZE = 100 * 1024 * 1024 + 1
UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt_secret = os.environ.get('JWT_SECRET_KEY')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')

storage = get_minio()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        # jwt_key = request.form.get('key')

        task_id = str(uuid.uuid4())

        logger.info({"Received": {"file": file,"task_id": task_id}})

        filename = str(uuid.uuid4())

        if file and allowed_file(file.filename):
            size = os.fstat(file.fileno()).st_size
            logger.info({"put to storage": file, "task_id": task_id})

            storage.put_object(
                "images", filename, file, length=-1, part_size=10*1024*1024
            )
 
            task_data = {
                "task_id": task_id,
                "filename": filename
            }

            try:
                logger.info(f'Задача {task_id} отправлена в очередь')

                send_to_queue(task_data, 'task_queue')

            except BaseException as e:
                logger.error(str(e), exc_info=True)
                raise

        logger.info({
            'status': 'task uploaded',
        })

    return render_template('index.html')


def download_file(output_img):
    logger.info({
        'status': 'Download file',
        'filename': output_img
    })
    return send_file(output_img, attachment_filename='image.jpg', as_attachment=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('FLASK_RUN_HOST'), port = os.environ.get('FLASK_RUN_PORT'))