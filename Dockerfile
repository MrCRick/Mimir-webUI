FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev mysql-server

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV FLASK_ENV=deployment
ENV MYSQL_HOST=172.30.0.2
ENV MYSQL_USER=rick
ENV MYSQL_DATABASE=mimir
ENV MYSQL_PASSWORD=password
ENV MYSQL_URL=mysql+pymysql://rick:password@172.30.0.2/

RUN pip3 install -r requirements.txt

COPY . /app

CMD flask run -h 0.0.0.0 -p 5000
