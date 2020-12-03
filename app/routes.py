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




@app.route('/notebookList', methods=['GET'])
def notebookList():
    if current_user.enable:
        res = requests.get(f'{app.config["APISERVER"]}/api/notebook').content
        all_notebook = json.loads(res)
        return render_template("notebookList.html", title="Notebook List", notebooks=all_notebook)
    else:
        return abort(404)



@app.route('/newNotebook', methods=['GET','POST'])
def newNotebook():
    if current_user.enable:
        if request.method == 'POST':
            res = requests.post(f'{app.config["APISERVER"]}/api/notebook', json={'notebook_name' : request.form.get('notebook_name')})

            if res.status_code == 201:
                flash(f'Notebook created!')
                print(res.text)
                return redirect(url_for('notebookList'))
            else:
                flash(f'Error..')
        return render_template("newNotebook.html", title="New Notebook")
    else:
        return abort(404)



@app.route('/deleteNotebook', methods=['POST'])
def deleteNotebook():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{app.config["APISERVER"]}/api/notebook/{id_to_delete}')

        if res.status_code == 200:
            flash(f'Notebook eliminated!')
            print(res.text)
        else:
            flash(f'Error..')

        return redirect(url_for('notebookList'))
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



@app.route('/newTraining', methods=['GET', 'POST'])
def newTraining():
    if current_user.enable:
        if request.method == 'POST':
            res = requests.post(f'{app.config["APISERVER"]}/api/training', json={'name' : request.form['name']})

            if res.status_code == 201:
                flash(f'Training created!')
                print(res.text)
                return redirect(url_for('trainingList'))
            else:
                flash(f'Error..')

        return render_template("newTraining.html", title="New Training")
    else:
        return abort(404)



@app.route('/deleteTraining', methods=['POST'])
def deleteTraining():
    if current_user.enable:
        id_to_delete = request.form['id_to_delete']
        res = requests.delete(f'{app.config["APISERVER"]}/api/training/{id_to_delete}')

        if res.status_code == 200:
            flash(f'Training eliminated!')
            print(res.text)
        else:
            flash(f'Error..')

        return redirect(url_for('trainingList'))
    else:
        return abort(404)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))