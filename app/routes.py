from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewNotebookForm, DeleteNotebookForm, NewTrainingForm, NewEndpointForm
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests
import json


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
            flash('Invalid email or password')
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



@app.route('/newNotebook', methods=['GET','POST'])
def newNotebook():
    form = NewNotebookForm()
    if form.validate_on_submit():
        notebook = {"name" : form.name.data}
        response = requests.post(f'{app.config["APISERVER"]}/api/notebook', data=json.dumps(notebook), headers={'Content-Type': 'application/json'})

        if response.status_code == 201:
            flash(f'Notebook created!')
        else:
            flash(f'Error..')
        
        print(response.status_code)
        print(response.text)
    return render_template("newNotebook.html", title="New Notebook", form=form)



@app.route('/notebookList', methods=['GET'])
def notebookList():
    res = requests.get(f'{app.config["APISERVER"]}/api/notebook').content
    all_notebook = json.loads(res)
    return render_template("notebookList.html", title="Notebook List", notebooks=all_notebook)



@app.route('/deleteNotebook', methods=['GET', 'DELETE'])
def deleteNotebook():
    form = DeleteNotebookForm()
    if form.validate_on_submit():
        notebook = {'ID' : form.id.data}
        res = requests.delete(f'{app.config["APISERVER"]}/api/notebook/<form.id.data>/',data=json.dumps(notebook), headers={'Content-Type': 'application/json'})

        if res.status_code == 200:
            flash(f'Notebook eliminated!')
        else:
            flash(f'Error..')

        print(res.status_code)
        print(res.content)
    return render_template("deleteNotebook.html", title="Delete Notebook", form=form)



@app.route('/newEndpoint', methods=['GET','POST'])
def newEndpoint():
    form = NewEndpointForm()
    if form.validate_on_submit():
        endpoint = {"name" : form.name.data, "trining_id": form.training_id.data}
        response = requests.post(f'{app.config["APISERVER"]}/api/endpoints', data=json.dumps(endpoint), headers={'Content-Type': 'application/json'})

        if response.status_code == 201:
            flash(f'Endpoint created!')
        else:
            flash(f'Error..')

        print(response.status_code)
        print(response.text)
    return render_template("newEndpoint.html", title="New Endpoint", form=form)



@app.route('/endpointList')
def endpointList():
    res = requests.get(f'{app.config["APISERVER"]}/api/endpoints').content
    all_endpoint = json.loads(res)
    return render_template("endpointList.html", title="Endpoint List", endpoints=all_endpoint)



@app.route('/newTraining', methods=['GET', 'POST'])
def newTraining():
    form = NewTrainingForm()
    if form.validate_on_submit():
        training = {"name" : form.name.data}
        response = requests.post(f'{app.config["APISERVER"]}/api/training', data=json.dumps(training), headers={'Content-Type': 'application/json'})

        if response.status_code == 201:
            flash(f'Training created!')
        else:
            flash(f'Error..')

        print(response.status_code)
        print(response.text)
    return render_template("newTraining.html", title="New Training", form=form)



@app.route('/trainingList')
def trainingList():
    res = requests.get(f'{app.config["APISERVER"]}/api/training').content
    all_training= json.loads(res)
    return render_template("trainingList.html", title="Training List", trainings=all_training)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


