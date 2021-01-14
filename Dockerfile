FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev mysql-server

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV FLASK_ENV=deployment

ENV MYSQL_USER=root
ENV MYSQL_DB=mimir
ENV MYSQL_HOST=mysql
ENV MYSQL_PASSWORD=secret

RUN pip3 install -r requirements.txt
RUN pip3 install --editable .
COPY . /app

CMD flask run -h 0.0.0.0 -p 5000