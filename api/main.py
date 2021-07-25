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
EXPORT_FOLDER = '/export'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt_secret = os.environ.get('JWT_SECRET_KEY')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')

storage = get_minio()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form.get('upload') == 'Upload':
            file = request.files['file']
            filename = request.form['filename']
            task_id = str(uuid.uuid4())
            logger.info({'Received': {'file': file,'task_id': task_id, 'filename': filename}})
            filename_uuid = str(uuid.uuid4())

            if file and allowed_file(file.filename):
                size = os.fstat(file.fileno()).st_size
                logger.info(f'put to storage {file}, task_id: {task_id}')
                storage.put_object('images', filename_uuid, file, length=-1, part_size=10*1024*1024)
                task_data = {'task_id': task_id,'filename': filename, 'filename_uuid':filename_uuid}

                try:
                    logger.info(f'Задача {task_id} отправлена в очередь')
                    send_to_queue(task_data, 'task_queue')
                except BaseException as e:
                    logger.error(str(e), exc_info=True)
                    raise

            logger.info('task uploaded')
            return render_template('index.html', uploadedFile=filename)

        elif request.form.get('downloadName') != '':
            filename = request.form['downloadName']
            return download_file(filename)         

    return render_template('index.html', uploadedFile='')


def download_file(filename):
    filename_processed = f'{filename}_detected'
    try:
        file = storage.get_object('images', filename_processed)
        logger.info(f'Download file {filename_processed}')
        return send_file(file, attachment_filename=f'{filename}.jpg', as_attachment=True)
    except BaseException as e:
        logger.error('File is not ready')
        return render_template('index.html', readyErr='File is not ready yet - try a bit later', uploadedFile=filename)


def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('FLASK_RUN_HOST'), port = os.environ.get('FLASK_RUN_PORT'))