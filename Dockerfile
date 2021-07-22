FROM python:3.7-stretch as prod

RUN mkdir -p /home/app

WORKDIR /home/app

ENV PYTHONUNBUFFERED="true"
ENV PYTHONPATH=/home/app

RUN apt-get update

# nodemon нужен на время разработки для перезапуска срипта при изменении файлов
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN npm i nodemon -g
RUN npm install pm2@latest -g

RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install flask
RUN pip install requests
RUN pip install uuid
RUN pip install pyjwt
RUN pip install aio-pika==6.6.1
RUN pip install pamqp==2.3.0
RUN pip install pika==1.1.0

COPY . .

ENV QUEUE_HOST=queue
ENV QUEUE_PORT=5672
ENV QUEUE_USERNAME=admin
ENV QUEUE_PASSWORD=admin1
ENV JWT_SECRET_KEY=2tlfkUkEMDdi6yPIp8EnA8wOFtNpiIbUh3UY0SgsjU6EUw9zaQDJ7joKzanQ2Dn
ENV JWT_ALGORITHM="HS256"

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST='0.0.0.0'
ENV FLASK_RUN_PORT=5000

EXPOSE $PORT

CMD ["pm2-runtime", "start", "ecosystem.config.js"]

FROM prod as dev
CMD ["nodemon", "--legacy-watch", "--exec", "python" , "main.py"]