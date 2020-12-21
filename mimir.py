from app import db
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
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
def list_users():
	"""Show all users"""
	db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
	cursor = db.cursor()
	click.echo('\n(USERNAME, EMAIL, ENABLE, IS_ADMIN)\n')
	cursor.execute('SELECT username, email, enable, is_admin FROM user')
	users = cursor.fetchall()
	db.close()
	
	for u in users:
		click.echo(u)
	click.echo('\n')



@cli.command('make-admin')
@click.argument('email')
def promote_user(email):
	"""Make a new admin"""
	user = User.query.filter_by(email=email).first_or_404(description='  User ({}) not found.\n'.format(email))

	db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
	cur = db.cursor()
	cur.execute('UPDATE user SET enable = True WHERE email = %s', (email,))
	cur.execute('UPDATE user SET is_admin = True WHERE email = %s', (email,))
	db.commit()
	click.echo('\nUser (' + email +') enabled and admin now.\n')



@cli.command('notebooks')
def notebooks():
	"""Show all notebooks"""
	res = requests.get(f'{APISERVER}/api/notebook').content
	click.echo(res)



@cli.command('create-notebook')
@click.argument('name')
def newNotebook(name):
	"""Create notebook"""
	res = requests.post(f'{APISERVER}/api/notebook', json = { 'name' : name })

	if res.status_code == 201:
		click.echo('\nNotebook created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



@cli.command('delete-notebook')
@click.argument('id_to_delete')
def deleteNotebook(id_to_delete):
	"""Delete notebook"""
	res = requests.delete(f'{APISERVER}/api/notebook/{id_to_delete}')

	if res.status_code == 200:
		click.echo('\nNotebook eliminated!\n')
	else:
		click.echo(res.status_code)



@cli.command('trainings')
def trainings():
	"""Show all trainings"""
	res = requests.get(f'{APISERVER}/api/training').content
	click.echo(res)



@cli.command('create-training')
@click.argument('name')
def newTraining(name):
	"""Create training"""
	res = requests.post(f'{APISERVER}/api/training', json = { 'name' : name })

	if res.status_code == 201:
		click.echo('\nTraining created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



@cli.command('delete-training')
@click.argument('id_to_delete')
def deleteTraining(id_to_delete):
	"""Delete training"""
	res = requests.delete(f'{APISERVER}/api/training/{id_to_delete}')

	if res.status_code == 200:
		click.echo('\nTraining eliminated!\n')
	else:
		click.echo(res.status_code)



@cli.command('endpoints')
def endpoints():
	"""Show all endpoints"""
	res = requests.get(f'{APISERVER}/api/endpoints').content
	click.echo(res)



@cli.command('create-endpoint')
@click.argument('name')
@click.argument('training_id')
def newEndpoint(name,training_id):
	"""Create endpoint"""
	res = requests.post(f'{APISERVER}/api/endpoints/endpoint', json = { 'name': name, 'training_id' : training_id })

	if res.status_code == 201:
		click.echo('\nEndpoint created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



@cli.command('delete-endpoint')
@click.argument('id_to_delete')
def deleteTraining(id_to_delete):
	"""Delete endpoint"""
	res = requests.delete(f'{APISERVER}/api/endpoint/{id_to_delete}')

	if res.status_code == 200:
		click.echo('\nEndpoint eliminated!\n')
	else:
		click.echo(res.status_code)