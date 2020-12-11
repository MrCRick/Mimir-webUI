from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests
import json
import os


APISERVER = os.environ.get("APISERVER")



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home Page")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)



@app.route('/profile/<username>')
@login_required
def user(username):
    user = Users.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title="Profile", user=user)



@app.route('/notebooks', methods=['GET'])
def notebooks():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/notebook').content
        all_notebook = json.loads(res)
        return render_template("notebooks.html", title="Notebooks", notebooks=all_notebook)
    else:
        return redirect(url_for('403'))



@app.route('/newNotebook', methods=['POST'])
def newNotebook():
    if current_user.enable:
        res = requests.post(f'{APISERVER}/api/notebook', json={'name' : request.form.get('name')})

        if res.status_code == 201:
            flash(f'Notebook created!')
        else:
            flash(res.status_code)
        return redirect(url_for('notebooks'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteNotebook', methods=['POST'])
def deleteNotebook():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/notebook/{id_to_delete}')

        if res.status_code == 200:
            flash(f'Notebook eliminated!')
        else:
            flash(res.status_code)
        return redirect(url_for('notebooks'))
    else:
        return redirect(url_for('403'))



@app.route('/trainings')
def trainings():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/training').content
        all_training= json.loads(res)
        return render_template("trainings.html", title="Trainings", trainings=all_training)
    else:
        return redirect(url_for('403'))



@app.route('/newTraining', methods=['POST'])
def newTraining():
    if current_user.enable:
        res = requests.post(f'{APISERVER}/api/training', json={'name' : request.form['name']})

        if res.status_code == 201:
            flash(f'Training created!')
        else:
            flash(res.status_code)
        return redirect(url_for('trainings'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteTraining', methods=['POST'])
def deleteTraining():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/training/{id_to_delete}')

        if res.status_code == 200:
            flash(f'Training eliminated!')
        else:
            flash(res.status_code)
        return redirect(url_for('trainings'))
    else:
        return redirect(url_for('403'))



@app.route('/endpoints', methods=['GET'])
def endpoints():
    if current_user.enable:
        res = requests.get(f'{APISERVER}/api/endpoints').content
        all_endpoint = json.loads(res)
        flash(f'Sorry, endpoints are not enabled.')
        return render_template("endpoints.html", title="Endpoint", endpoints=all_endpoint)
    else:
        return redirect(url_for('403'))



@app.route('/newEndpoint', methods=['POST'])
def newEndpoint():
    if current_user.enable:
        res = requests.post(f'{APISERVER}/api/endpoints/endpoint', json={'name': request.form['name'], 'training_id' : request.form['training_id']})

        if res.status_code == 201:
            flash(f'Endpoint created!')
        else:
            flash(res.status_code)
        return redirect(url_for('endpoints'))
    else:
        return redirect(url_for('403'))



@app.route('/deleteEndpoint', methods=['POST'])
def deleteEndpoint():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{APISERVER}/api/endpoint/{id_to_delete}')

        if res.status_code == 200:
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
