FROM ubuntu:latest
WORKDIR /app
COPY . /app
RUN apt-get -y update && apt-get -y upgrade
RUN pip install requirements.txt
ENTRYPOINT ["python"]
CMD [-m flask run"]