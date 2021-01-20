# Mimir-webUI

Mimir-webUI is a web application used to create notebooks, trainings, and (in the future) endpoints. 

How to Use
==========

Prerequisites
-------------

You need to install:

	Python
	MySQL
	Pip
	Pipenv



Create virtual environment
--------------------------

Install all repository dependencies:

    $ pipenv install --dev

Create a virtual env with command:

    $ pipenv shell
   


Create database
---------------

In terminal of your Mimir-webUI virtual env:

	$ python build_DB.py

Now you created your mimir DB.



Set environment variables
-------------------------

Create some variables to connect WebUI to Api Server:

    $ nano ~/.bashrc
    
At the end set variables: 

	export MYSQL_HOST="mysql host"
	export MYSQL_USER="mysql user"
	export MYSQL_DB="mysql db name"
	export MYSQL_PASSWORD="mysql password"
	export MYSQL_URL=mysql+pymysql://"mysql user":"mysql password"@"mysql host"/"mysql db name"
	export DOMAIN_NAME=.notebooks.kubernetes.local
	export CELERY_BROKER=pyamqp://guest@localhost//
	export CELERY_BACKEND=rpc://
	export MINIO_ACCESS_KEY=admin
	export MINIO_SECRET_KEY=keystone
	export ENDPOINT=http://192.168.49.2:31000
	export BUCKET=bucket
	export APISERVER=http://"api server ip address and port"
	export PATH_FOLDER="where download file for training"
	export UPLOAD_FILE="where upload file for training"

Save the changes:
	
	$ source ~/.bashrc    



Running It
----------

In your virtual env:

    $ flask run



Cli
----
If you want to create, destroy or view the list of notebook and training from your cli, you need to use this command in the virtual environment:

	$ pip install --editable .

Then you with the command:

	$ mimir

can see other commands.



And then..
----------

Now in order for everything to work, you need to download two more Git repository:

1 Mimir-ApiServer: https://github.com/dandamico/Mimir-ApiServer

2 Mimir-Engine: https://github.com/FedericoGiuliana/Mimir-Engine



Dockerize flask app
===================


Prerequisites:
--------------

You need to install:

	Docker
	Minikube



Start minikube:
	
	$ minikube start



Create network, images and containers
-------------------------------------

Now you need to create one image for each container.
We need one image and container for Mimir-webUI and one image and container for mysql and connect each other through a network.

Create a new network:

	$ docker network create mimir_network


Create and run container for mysql:

	$ docker run -d \
		--name mimir_webui_container \
		--network mimir_network --network-alias mysql \
		-e MYSQL_ROOT_PASSWORD="mysql password" \
		-e MYSQL_DATABASE="mysql database name" \
		mysql


Now you created mysql image and container.


In your directory you have a Dockerfile that we'll use to create a Docker image. In Mimir-webUI directory use this command:

	$ docker build -f Dockerfile -t mimir_webui .


Now create a container Docker:

	$ docker run -dp 5000:5000 \
		--network mimir_network \
		-e FLASK_ENV=deployment \
		-e MYSQL_HOST= "mysql host" \
		-e MYSQL_USER= "mysql user" \
		-e MYSQL_PASSWORD= "mysql password" \
		-e MYSQL_DB=mimir \
		-e MYSQL_URL=mysql+pymysql://"mysql user":"mysql password"@mysql/mimir \
		-e APISERVER=http://"apiserver container name":"apiserver port" \
		-e PATH_FOLDER=/"path where download file for training" \
		-e UPLOAD_FILE=/"path where upload file for training" \
		mimir_webui

Now with command:
	
	$ docker ps 

You can see 2 new container: mimir_webui_container and mysql.

Run the command to start the container:

	$ docker logs -f mimir_webui_container


For everything to work, you need an active api server.

You need to download two more Git repository:

1 Mimir-ApiServer: https://github.com/dandamico/Mimir-ApiServer

2 Mimir-Engine: https://github.com/FedericoGiuliana/Mimir-Engine