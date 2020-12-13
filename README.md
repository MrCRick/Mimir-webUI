# Mimir-webUI

Mimir-webUI is a web application used to create notebooks, training, and (in the future) endpoints.

How to Use
==========

Prerequisites
-------------

You need to install:

Miniconda: 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

Sqlite3 and sqlitebrowser:

https://linuxhint.com/install_sqlite_browser_ubuntu/

Pip: 

    $ sudo apt install python-pip
    
Pipenv:

    $ pip install pipenv
   

Create virtual environment
--------------------------

In your directory create a virtual env with command:

    $ pipenv shell
    

Now in your virtual env install all dependencies:

    $ pipenv install --dev
    


Create database
---------------

In your virtual env:

	$ flask db init

	$ flask db migrate -m "(table name) table"

	$ flask db upgrade

Now you created a DB in your repository.


Set environment variables
-------------------------

Create some variables to connect WebUI to Api Server:

    $ nano ~/.bashrc
    
At the end set variables: 

	export APISERVER="ip address of the api server that you choice"

Save the changes:
	
	$ source ~/.bashrc    



Running It
----------

In your virtual env:

    $ python -m flask run



And then..
----------

Now in order for this performance to work, you need to download two more Git repository: Mimir-ApiServer and Mimir-Engine:

1 Mimir-ApiServer: https://github.com/dandamico/Mimir-ApiServer

2 Mimir-Engine: https://github.com/FedericoGiuliana/Mimir-Engine