from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Contributor

# Form used to register a new contributor
class RegistrationForm(FlaskForm):
    name = StringField('Name', 
                            validators=[DataRequired()])
    surname = StringField('Surname', 
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        contributor = Contributor.query.filter_by(email = email.data).first()
        if contributor:
            raise ValidationError('That email is already registered. Please choose another one.')

# Form used to login to the contributor interface
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Form used to update account information
# /!\ 18.01: need to include option to modify password
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', 
                            validators=[DataRequired()])
    surname = StringField('Surname', 
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
              raise ValidationError('That email is already registered. Please choose another one.')

