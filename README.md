# Mimir-webUI

Mimir-webUI is a web application used to create notebooks, trainings, and (in the future) endpoints.

How to Use
==========

Prerequisites
-------------

You need to install:

Miniconda:

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

MySQL:

https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

Pip: 

    $ sudo apt install python-pip
    
Pipenv:

    $ pip install pipenv
   

Create virtual environment
--------------------------

Install all repository dependencies:

    $ pipenv install --dev

Create a virtual env with command:

    $ pipenv shell
   
   
Create database
---------------

First following this repository to create mimir DataBase: https://github.com/dandamico/Mimir-ApiServer.git

Then in terminal of your Mimir-webUI virtual env:

	$ python build_tables.py

Now you created two tables in mimir DB.


Set environment variables
-------------------------

Create some variables to connect WebUI to Api Server:

    $ nano ~/.bashrc
    
At the end set variables: 

	export MYSQL_HOST="mysql host"
	export MYSQL_USER="mysql user"
	export MYSQL_PASSWORD="mysql password"
	export MYSQL_URL=mysql+pymysql://"mysql user":"mysql password"@"mysql host"/
	export DOMAIN_NAME=.notebooks.kubernetes.local
	export CELERY_BROKER=pyamqp://guest@localhost//
	export CELERY_BACKEND=rpc://
	export APISERVER=http://"api server ip address and port"
	export PATH_FOLDER="where download file for training"
	export UPLOAD_FILE="where upload file for training"

Save the changes:
	
	$ source ~/.bashrc    



Running It
----------

In your virtual env:

    $ python -m flask run



Cli
----
If you want to create, destroy or view the list of notebook and training from your cli, you need to use this command in the virtual environment:

	$ pip install --editable .

Then you with the command:

	$ mimir

can see other commands.



And then..
----------

Now in order for this performance to work, you need to download two more Git repository: Mimir-ApiServer and Mimir-Engine:

1 Mimir-ApiServer: https://github.com/dandamico/Mimir-ApiServer

2 Mimir-Engine: https://github.com/FedericoGiuliana/Mimir-Engine
