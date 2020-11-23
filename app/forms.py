from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Users



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



class NewNotebookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')



class DeleteNotebookForm(FlaskForm):
    notebook_id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Delete')



class NewTrainingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')



class DeleteTrainingForm(FlaskForm):
    training_id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Delete')



class UpdateTrainingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    training_id = StringField('Training_id', validators=[DataRequired()])
    submit = SubmitField('Update')



class NewEndpointForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    training_id = StringField('Training_id', validators=[DataRequired()])
    submit = SubmitField('Create')



class DeleteEndpointForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Delete')