from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import config
import os


MYSQL_URL=os.environ.get("MYSQL_URL")


app = Flask(__name__)
admin = Admin(app, name="Control Panel")

app.config["SECRET_KEY"] = 'you-will-never-guess'
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URL+"mimir"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login = LoginManager(app)


from app import routes, models, errors
from app.models import User, Controller


admin.add_view(Controller(User, db.session))


if '__name__' == '__main__':
	app.run(debug=True)
