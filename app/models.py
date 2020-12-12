from app import db, login
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView



class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    enable = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Users {}>'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    @login.user_loader
    def load_user(id):
    	return Users.query.get(int(id))



class Controller(ModelView):
    
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)

    def not_auth(self):
        return "you are not abilitated to use this admin panel control"



    
