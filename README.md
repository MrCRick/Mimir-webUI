# Mimir-webUI


How to Use
==========

Prerequisites
-------------

You need to install:

1 Miniconda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

2 Pip: 

    $ sudo apt install python-pip
    
3 Pipenv:

    $ pip install pipenv
   

In your directory create a virtual env with command:

    $ pipenv shell
    

Now in your virtual env install all dependencies:

    $ pipenv install --dev
    

Set environment variables to connect WebUI to Api Server:

    $ nano ~/.bashrc
    
At the end set variables: 

	export APISERVER="ip address of the api server you choice"

Save the changes:
	
	$ source ~/.bashrc    


Running It
----------

In your virtual env:

    $ python -m flask run
