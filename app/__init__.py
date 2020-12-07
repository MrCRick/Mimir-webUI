from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
admin = Admin(app, name="Control Panel")

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


from app import routes, models, errors
from app.models import Users, Controller


admin.add_view(Controller(Users, db.session))


if '__name__' == '__main__':
	app.run(debug=True)