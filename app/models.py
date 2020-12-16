from app import db, login
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView



class User(UserMixin, db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    enable = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)



    def serialize(self):
       return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "enable": self.enable,
            "is_admin": self.is_admin
       }



    def deserialize(self, data):
        for field in ['id', 'username', 'email', 'password_hash', 'enable', 'is_admin']:
            if field in data:
                setattr(self, field, data[field])


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)



    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




class Object_ID(db.Model):
    __tablename__= "user_object_id"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    notebook_id = db.Column(db.Integer)
    training_id = db.Column(db.Integer)
    endpoint_id = db.Column(db.Integer)



    def __repr__(self):
        return '<Object_ID {}>'.format(self.user_id)



    def serialize(self):
       return{
            "id": self.id,

       }



    def deserialize(self, data):
        for field in ['id', 'user_id', 'notebook_id', 'training_id', 'endpoint_id']:
            if field in data:
                setattr(self, field, data[field])




class Controller(ModelView):
    
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)

    def not_auth(self):
        return "you are not abilitated to use this admin panel control"



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
