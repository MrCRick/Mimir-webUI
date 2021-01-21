FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install --editable .

CMD flask run -h 0.0.0.0 -p 5000
