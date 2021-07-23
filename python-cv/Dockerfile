FROM python:3.9-buster as base

RUN mkdir -p /home/app

WORKDIR /home/app

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install ffmpeg libsm6 libxext6  -y

# nodemon нужен на время разработки для перезапуска срипта при изменении файлов
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN npm i nodemon -g
RUN npm install pm2@latest -g

RUN pip install requests
RUN pip install uuid
RUN pip install minio
RUN pip install aio-pika==6.6.1
RUN pip install pamqp==2.3.0
RUN pip install pika==1.1.0
RUN pip install redis
RUN pip install opencv-python

COPY . .

ENV QUEUE_HOST=queue
ENV QUEUE_PORT=5672
ENV QUEUE_USERNAME=admin
ENV QUEUE_PASSWORD=admin1

ENV MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
ENV MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
ENV MINIO_ENDPOINT=localhost:9000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST='0.0.0.0'
ENV FLASK_RUN_PORT=5000

ENV PYTHONUNBUFFERED="true"

EXPOSE $PORT

CMD ["pm2-runtime", "start", "ecosystem.config.js"]

FROM base as dev
CMD ["nodemon", "--legacy-watch", "--exec", "python" , "main.py"]
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development

FROM base as prod
CMD ["nodemon", "--legacy-watch", "--exec", "python" , "main.py"]
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development