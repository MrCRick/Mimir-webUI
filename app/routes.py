from flask import render_template, flash, redirect, url_for, request, jsonify, make_response, abort
from app import app, db
from app.forms import LoginForm, RegistrationForm
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



#notebook = {"name":"pippo", "id":"12345"}

#response = requests.get("http://0.0.0.0:5000/api/notebooks", data=json.dumps(notebook), headers={'Content-Type': 'application/json'})
#response = requests.get("http://0.0.0.0:5000/api/notebook/12345", data=json.dumps(notebook), headers={'Content-Type': 'application/json'})
#response = requests.post("http://0.0.0.0:5000/api/notebook/12345", data=json.dumps(notebook), headers={'Content-Type': 'application/json'})
#response = requests.put("http://0.0.0.0:5000/api/notebook/12345", data=json.dumps(notebook), headers={'Content-Type': 'application/json'})
#response = requests.delete("http://0.0.0.0:5000/api/notebook/12345", data=json.dumps(notebook), headers={'Content-Type': 'application/json'})



@app.route('/newNotebook', methods=['GET','POST'])
def newNotebook():
    if current_user.enable:
        if request.method == 'POST':
            notebook = {'name' : request.form['name']}
            res = requests.post(f'{app.config["APISERVER"]}/api/notebook', json=notebook)

            if res.status_code == 201:
                flash(f'Notebook created!')
                print(res.text)
            else:
                flash(f'Error..')
        return render_template("newNotebook.html", title="New Notebook")
    else:
        return abort(404)



@app.route('/notebookList', methods=['GET'])
def notebookList():
    if current_user.enable:
        res = requests.get(f'{app.config["APISERVER"]}/api/notebook').content
        all_notebook = json.loads(res)
        return render_template("notebookList.html", title="Notebook List", notebooks=all_notebook)
    else:
        return abort(404)



@app.route('/deleteNotebook', methods=['GET','POST'])
def deleteNotebook():
    if current_user.enable:
        res = requests.delete(f'{app.config["APISERVER"]}/api/notebook/1')

        if res.status_code == 200:
            flash(f'Notebook eliminated!')
            print(res.text)
        else:
            flash(f'Error..')

        return render_template("deleteNotebook.html", title="Delete Notebook")
    else:
        return abort(404)



@app.route('/newEndpoint', methods=['GET','POST'])
def newEndpoint():
    if current_user.enable:
        if request.method == 'POST':
            endpoint = {'name' : request.form['name'], 'training_id': request.form['training_id']}
            res = requests.post(f'{app.config["APISERVER"]}/api/endpoints/endpoint', data=json.dumps(endpoint), headers={'Content-Type': 'application/json'})

            if res.status_code == 201:
                flash(f'Endpoint created!')
                print(res.text)
            else:
                flash(f'Error..')

        return render_template("newEndpoint.html", title="New Endpoint")
    else:
        return abort(404)



@app.route('/endpointList')
def endpointList():
    if current_user.enable:
        res = requests.get(f'{app.config["APISERVER"]}/api/endpoints').content
        all_endpoint = json.loads(res)
        return render_template("endpointList.html", title="Endpoint List", endpoints=all_endpoint)
    else:
        return abort(404)



@app.route('/newTraining', methods=['GET', 'POST'])
def newTraining():
    if current_user.enable:
        if request.method == 'POST':
            training = {'name' : request.form['name']}
            res = requests.post(f'{app.config["APISERVER"]}/api/training', data=json.dumps(training), headers={'Content-Type': 'application/json'})

            if res.status_code == 201:
                flash(f'Training created!')
                print(res.text)
            else:
                flash(f'Error..')

        return render_template("newTraining.html", title="New Training")
    else:
        return abort(404)



@app.route('/trainingList')
def trainingList():
    if current_user.enable:
        res = requests.get(f'{app.config["APISERVER"]}/api/training').content
        all_training= json.loads(res)
        return render_template("trainingList.html", title="Training List", trainings=all_training)
    else:
        return abort(404)



@app.route('/deleteTraining', methods=['GET'])
def deleteTraining():
    if current_user.enable:
        
        training = {'training_id' : request.form['training_id']}
        res = requests.delete(f'{app.config["APISERVER"]}/api/training/1',data=json.dumps(training), headers={'Content-Type': 'application/json'})

        if res.status_code == 200:
            flash(f'Training eliminated!')
            print(res.text)
        else:
            flash(f'Error..')

        return render_template("deleteTraining.html", title="Delete Training")
    else:
        return abort(404)



@app.route('/updateTraining', methods=['GET'])
def updateTraining():
    if current_user.enable:
        training = {'name' : request.form['name'], 'training_id' : request.form['training_id']}
        res = requests.put(f'{app.config["APISERVER"]}/api/training/request.form.get(training_id)', data=json.dumps(training), headers={'Content-Type': 'application/json'})

        if res.status_code == 200:
            flash(f'Training updated!')
            print(res.text)
        else:
            flash(f'Error..')

        return render_template("updateTraining.html", title="Update Training")
    else:
        return abort(404)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


