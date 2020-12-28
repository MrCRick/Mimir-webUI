from app import db
from app.models import User
import mysql.connector as mysql
import requests
import json
import os
import click



APISERVER = os.environ.get("APISERVER")
MYSQL_HOST=os.environ.get("MYSQL_HOST")
MYSQL_PSSW=os.environ.get("MYSQL_PASSWORD")
MYSQL_USER=os.environ.get("MYSQL_USER")
MYSQL_URL=os.environ.get("MYSQL_URL")



@click.group()
def cli():
    pass



@cli.command('users')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def list_users(username, password):
	"""Show all users"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.is_admin == True:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cursor = db.cursor()
			cursor.execute('SELECT username, email, enable, is_admin FROM user')
			users = cursor.fetchall()
			db.close()

			for u in users:
				click.echo(u)
		else:
			click.echo('Access denied.')
	else:
		click.echo('Invalid password')



@cli.command('make-admin')
@click.option('--email', prompt='Admin email')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def promote_user(email,username,password):
	"""Make a new admin"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):

		db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
		cur = db.cursor()
		cur.execute('SELECT COUNT(*) FROM user')
		users = cur.fetchone()

		if users == (1,):
			cur.execute('UPDATE user SET enable = True WHERE email = %s', (email,))
			cur.execute('UPDATE user SET is_admin = True WHERE email = %s', (email,))
			db.commit()
			db.close()
			click.echo('User (' + email +') enabled and admin now.')
		else:
			click.echo('Access denied.')
	else:
		click.echo('Invalid password')



@cli.command('notebooks')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def notebooks(username,password):
	"""Show your notebook list"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id')
			objects = cur.fetchall()
			db.close()

			notebooks = []
			for notebook in objects:
				if notebook[3] == user.username and notebook[2] == "notebook":
					notebook_id = notebook[1]

					res = requests.get(f'{APISERVER}/api/notebook/{notebook_id}').content
					notebook = json.loads(res)

					notebooks.append(notebook)
				else:
					if user.is_admin and notebook[2] == "notebook":
						notebook_id = notebook[1]

						res = requests.get(f'{APISERVER}/api/notebook/{notebook_id}').content
						notebook = json.loads(res)

						notebooks.append(notebook)

			click.echo(notebooks)
		else:
			click.echo('You can\'t create notebook')
	else:
		click.echo('Invalid password')



@cli.command('create-notebook')
@click.option('--name', prompt='Notebook name')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def newNotebook(username,name,password):
	"""Create a new notebook"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:
			res = requests.post(f'{APISERVER}/api/notebook', json = { 'name' : name })

			if res.status_code == 201:

				dates = json.loads(res.text)
				notebook_id = dates.get('id')

				db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
				cur = db.cursor()
				cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (notebook_id, "notebook", user.username,))
				db.commit()
				db.close()

				click.echo('Notebook created!\n')
				click.echo(res.content)
			else:
				click.echo(res.status_code)
		else:
			click.echo('You can\'t create notebook')
	else:
		click.echo('Invalid password')



@cli.command('delete-notebook')
@click.option('--id_to_delete', prompt="Notebook id")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def deleteNotebook(username,id_to_delete,password):
	"""Delete notebook"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id WHERE user_name = %s AND object_id = %s', (user.username, id_to_delete))
			notebook_to_delete = cur.fetchone()
			db.close()

			if notebook_to_delete:
				res = requests.delete(f'{APISERVER}/api/notebook/{id_to_delete}')

				if res.status_code == 200:

					db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
					cur = db.cursor()
					cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"notebook",))
					db.commit()
					db.close()

					click.echo('Notebook eliminated')
				else:
					click.echo(res.status_code)
			else:
				click.echo('Invalid notebook_id')
		else:
			click.echo('You can\'t delete notebook')
	else:
		click.echo('Invalid password')



@cli.command('trainings')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def trainings(username,password):
	"""Show your training list"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable == True:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id')
			objects = cur.fetchall()
			db.close()

			trainings = []
			for training in objects:
				if training[3] == user.username and training[2] == "training":
					training_id = training[1]

					res = requests.get(f'{APISERVER}/api/training/{training_id}').content
					training = json.loads(res)

					trainings.append(training)
				elif user.is_admin and training[2] == "training":
						training_id = training[1]
						res = requests.get(f'{APISERVER}/api/training/{training_id}').content
						training = json.loads(res)

						trainings.append(training)
			click.echo(trainings)
		else:
			click.echo('You can\'t create training')
	else:
		click.echo('Invalid password')



@cli.command('create-training')
@click.argument('file', type=click.File('r'))
@click.option('--name', prompt="Training name")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def newTraining(username,name,file,password):
	"""Create a new training"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:
			files = {'file': file}

			res = requests.post(f'{APISERVER}/api/training/{name}',files=files)

			if res.status_code == 201:

				dates = json.loads(res.text)
				training_id = dates.get('id')

				db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
				cur = db.cursor()
				cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (training_id, "training", user.username,))
				db.commit()
				db.close()

				click.echo('Training created!\n')
				click.echo(res.content)
			else:
				click.echo(res.status_code)
		else:
			click.echo('You can\'t create training')
	else:
		click.echo('Invalid password')



@cli.command('delete-training')
@click.option('--id_to_delete',prompt="Training id")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def deleteTraining(username,id_to_delete,password):
	"""Delete training"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id WHERE user_name = %s AND object_id = %s', (user.username, id_to_delete))
			training_to_delete = cur.fetchone()
			db.close()

			if training_to_delete:
				res = requests.delete(f'{APISERVER}/api/training/{id_to_delete}')

				if res.status_code == 200:

					db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
					cur = db.cursor()
					cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"training",))
					db.commit()
					db.close()

					click.echo('Training eliminated')
				else:
					click.echo(res.status_code)
			else:
				click.echo('Invalid training_id')
		else:
			click.echo('You can\'t delete training')
	else:
		click.echo('Invalid password')


@cli.command('endpoints')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def endpoints(username,password):
	"""Show your endpoint list"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id')
			objects = cur.fetchall()
			db.close()

			endpoints = []
			for endpoint in objects:
				if endpoint[3] == user.username and endpoint[2] == "endpoint":
					endpoint_id = endpoint[1]

					res = requests.get(f'{APISERVER}/api/endpoint/{endpoint_id}').content
					endpoint = json.loads(res)

					endpoints.append(endpoint)
				else:
					if user.is_admin and endpoint[2] == "endpoint":
						endpoint_id = endpoint[1]

						res = requests.get(f'{APISERVER}/api/endpoint/{endpoint_id}').content
						endpoint = json.loads(res)

						endpoints.append(endpoint)

			click.echo(endpoints)
		else:
			click.echo('You can\'t create endpoint')
	else:
		click.echo('Invalid password')



@cli.command('create-endpoint')
@click.option('--name', prompt="Enpoint name")
@click.option('--training_id', prompt="Training id")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def newEndpoint(username,name,training_id,password):
	"""Create a new endpoint"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:
			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id WHERE object_id =%s AND object_type=%s AND user_name=%s',(training_id,"training", user.username,))
			training = cur.fetchone()
			db.close()

			if training == None:
				click.echo('Invalid training id')
			else:
				training_id = training[1]

				res = requests.post(f'{APISERVER}/api/endpoints/endpoint', json = { 'name': name, 'training_id' : training_id })

				if res.status_code == 201:

					dates = json.loads(res.text)
					endpoint_id = dates.get('id')

					db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
					cur = db.cursor()
					cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (endpoint_id, "endpoint", user.username,))
					db.commit()
					db.close()
					
					click.echo('Endpoint created\n')
					click.echo(res.content)
				else:
					click.echo(res.status_code)
		else:
			click.echo('You can\'t create endpoint')
	else:
		click.echo('Invalid password')



@cli.command('delete-endpoint')
@click.option('--id_to_delete', prompt="Endpoint id")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def deleteTraining(username,id_to_delete,password):
	"""Delete endpoint"""
	user = User.query.filter_by(username=username).first_or_404(description='Invalid username')

	if user.check_password(password):
		if user.enable:

			db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
			cur = db.cursor()
			cur.execute('SELECT * FROM user_object_id WHERE user_name = %s AND object_id = %s', (user.username, id_to_delete))
			endpoint_to_delete = cur.fetchone()
			db.close()

			if endpoint_to_delete:
				res = requests.delete(f'{APISERVER}/api/endpoint/{id_to_delete}')

				if res.status_code == 200:

					db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
					cur = db.cursor()
					cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"notebook",))
					db.commit()
					db.close()

					click.echo('\nEndpoint eliminated!\n')
				else:
					click.echo(res.status_code)
			else:
				click.echo('Invalid endpoint_id')
		else:
			click.echo('You can\'t delete endpoint')
	else:
		click.echo('Invalid password')