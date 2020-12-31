from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import Sheet, Contributor, Author, Article, Result
from flask_wtf.file import FileField, FileAllowed

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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

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

class FactSheetForm(FlaskForm):
    policy = StringField('Policy', validators=[DataRequired()])
    target = StringField('Target', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
    picture = FileField('Add a Picture', validators=[FileAllowed(['jpg','png'])])
    save = SubmitField('Save')
    submit = SubmitField('Submit')
    publish = SubmitField('Publish')
    creation = DateField('Creation Date', validators=[DataRequired()])
    update = DateField('Date Updated', validators=[DataRequired()])
    result = SelectField('Select Results', choices=[], coerce=int)