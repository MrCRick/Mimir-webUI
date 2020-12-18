from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import mysql.connector as mysql
import requests
import json
import os
import sqlite3


MYSQL_HOST=os.environ.get("MYSQL_HOST")
MYSQL_PSSW=os.environ.get("MYSQL_PASSWORD")
MYSQL_USER=os.environ.get("MYSQL_USER")
MYSQL_URL=os.environ.get("MYSQL_URL")
APISERVER = os.environ.get("APISERVER")



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home Page")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)



@app.route('/profile/<username>')
@login_required
def user(username):
    if current_user.username != username:
        return redirect(url_for('index'))
    else:
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('user.html', title="Profile", user=user)



@app.route('/notebooks', methods=['GET'])
@login_required
def notebooks():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/notebook').content
        all_notebook = json.loads(res)
        return render_template("notebooks.html", title="Notebooks", notebooks=all_notebook)
    else:
        return redirect(url_for('403'))



@app.route('/newNotebook', methods=['POST'])
@login_required
def newNotebook():
    if current_user.enable:
        res = requests.post(f'{APISERVER}/api/notebook', json={'name' : request.form['name']})

        if res.status_code == 201:

            dates = json.loads(res.text)
            notebook_id = dates.get('id')

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (notebook_id, "notebook", current_user.username,))
            db.commit()
            db.close()

            flash(f'Notebook created!')
        else:
            flash(res.status_code)
        return redirect(url_for('notebooks'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteNotebook', methods=['POST'])
@login_required
def deleteNotebook():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/notebook/{id_to_delete}')

        if res.status_code == 200:

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"notebook",))
            db.commit()
            db.close()

            flash(f'Notebook eliminated!')
        else:
            flash(res.status_code)
        return redirect(url_for('notebooks'))
    else:
        return redirect(url_for('403'))



@app.route('/trainings')
@login_required
def trainings():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/training').content
        all_training= json.loads(res)
        return render_template("trainings.html", title="Trainings", trainings=all_training)
    else:
        return redirect(url_for('403'))



@app.route('/newTraining', methods=['POST'])
@login_required
def newTraining():
    if current_user.enable:
        name = request.form['name']
        files = {'file': request.files['file'].name}
        res = requests.post(f'{APISERVER}/api/training/{name}', files=files)

        if res.status_code == 201:

            dates = json.loads(res.text)
            training_id = dates.get('id')

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (training_id, "training", current_user.username,))
            db.commit()
            db.close()

            flash(f'Training created!')
        else:
            flash(res.status_code)
        return redirect(url_for('trainings'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteTraining', methods=['POST'])
@login_required
def deleteTraining():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/training/{id_to_delete}')

        if res.status_code == 200:

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"training",))
            db.commit()
            db.close()

            flash(f'Training eliminated!')
        else:
            flash(res.status_code)
        return redirect(url_for('trainings'))
    else:
        return redirect(url_for('403'))



@app.route('/endpoints', methods=['GET'])
@login_required
def endpoints():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/endpoints').content
        all_endpoint = json.loads(res)
        flash(f'Sorry, endpoints are not enabled.')
        return render_template("endpoints.html", title="Endpoint", endpoints=all_endpoint)
    else:
        return redirect(url_for('403'))



@app.route('/newEndpoint', methods=['POST'])
@login_required
def newEndpoint():
    if current_user.enable:
        res = requests.post(f'{APISERVER}/api/endpoints/endpoint', json={'name': request.form['name'], 'training_id' : request.form['training_id']})

        if res.status_code == 201:

            dates = json.loads(res.text)
            endpoint_id = dates.get('id')

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('INSERT INTO user_object_id (object_id, object_type, user_name) VALUES (%s,%s,%s)', (endpoint_id, "endpoint", current_user.username,))
            db.commit()
            db.close()

            flash(f'Endpoint created!')
        else:
            flash(res.status_code)
        return redirect(url_for('endpoints'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteEndpoint', methods=['POST'])
@login_required
def deleteEndpoint():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/endpoint/{id_to_delete}')

        if res.status_code == 200:

            db = mysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PSSW,database='mimir')
            cur = db.cursor()
            cur.execute('DELETE FROM user_object_id WHERE object_id = %s AND object_type = %s', (id_to_delete,"endpoint",))
            db.commit()
            db.close()

            flash(f'Endpoint eliminated!')
        else:
            flash(res.status_code)
        return redirect(url_for('endpoints'))
    else:
        return redirect(url_for('403'))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
