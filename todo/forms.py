from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from todo.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('LogIn')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 8, max = 60)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()

        if email:
            raise ValidationError('Email already exist!')
        
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Username already exist!')

class AddTaskForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(min = 2, max = 30)])
    description = StringField('Description', validators = [DataRequired()])
    submit = SubmitField('Add')

class UpdateTaskForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(min = 2, max = 30)])
    description = StringField('Description', validators = [DataRequired()])
    submit = SubmitField('Update')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    image = FileField('Update profile image', validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')