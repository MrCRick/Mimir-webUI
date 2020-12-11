from flask import flash
from app import db
from app.models import Users
import sqlite3 as sql
import requests
import json
import os
import click



APISERVER = os.environ.get("APISERVER")



@click.group()
def cli():
    pass



#Show users
@cli.command('list-users')
def list_users():
	con = sql.connect("app.db")
	cur = con.cursor()
	cur.execute('SELECT * FROM Users')
	users = cur.fetchall()

	for u in users:
		click.echo(u)



# add command to promote first user on an empty DB
@cli.command('make-admin')
@click.argument('email')
def promote_user(email):
	user = Users.query.filter_by(email=email).first_or_404()
	if email is not email:
		click.echo("The user "+email+" found.")
	else:
		con = sql.connect("app.db")
		con.execute('UPDATE Users SET enable = True WHERE email = ?',(email,))
		con.execute('UPDATE Users SET is_admin = True WHERE email = ?',(email,))
		con.commit()
		click.echo("The user "+email+" enabled and is admin now.")



#Show list notebook
@cli.command('list-notebook')
def notebooks():
	res = requests.get(f'{APISERVER}/api/notebook').content
	click.echo(res)



#Create new notebook
@cli.command('create-notebook')
@click.argument('name')
def newNotebook(name):
	res = requests.post(f'{APISERVER}/api/notebook', json={'name':name})

	if res.status_code == 201:
		click.echo('\nNotebook created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



#Delete notebook
@cli.command('delete-notebook')
@click.argument('id_to_delete')
def deleteNotebook(id_to_delete):
	res = requests.delete(f'{APISERVER}/api/notebook/{id_to_delete}')

	if res.status_code == 200:
		click.echo('\nNotebook eliminated!\n')
	else:
		click.echo(res.status_code)



#Show list training
@cli.command('list-training')
def trainings():
	res = requests.get(f'{APISERVER}/api/training').content
	click.echo(res)



#Create a new Training
@cli.command('create-training')
@click.argument('name')
def newTraining(name):
	res = requests.post(f'{APISERVER}/api/training', json={'name' : name})

	if res.status_code == 201:
		click.echo('\nTraining created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



#Delete Training
@cli.command('delete-training')
@click.argument('id_to_delete')
def deleteTraining(id_to_delete):
    res = requests.delete(f'{APISERVER}/api/training/{id_to_delete}')

    if res.status_code == 200:
        click.echo('\nTraining eliminated!\n')
    else:
        click.echo(res.status_code)



#Show list endpoints
@cli.command('list-endpoint')
def endpoints():
	res = requests.get(f'{APISERVER}/api/endpoints').content
	click.echo(res)



#Create new endpoint
@cli.command('create-endpoint')
@click.argument('name')
@click.argument('training_id')
def newEndpoint(name,training_id):
	res = requests.post(f'{APISERVER}/api/endpoints/endpoint', json={'name': name, 'training_id' : training_id })

	if res.status_code == 201:
		click.echo('\nEndpoint created!\n')
		click.echo(res.content)
	else:
		click.echo(res.status_code)



#Delete endpoint
@cli.command('delete-endpoint')
@click.argument('id_to_delete')
def deleteTraining(id_to_delete):
	res = requests.delete(f'{APISERVER}/api/endpoint/{id_to_delete}')

	if res.status_code == 200:
		click.echo('\nEndpoint eliminated!\n')
	else:
		click.echo(res.status_code)