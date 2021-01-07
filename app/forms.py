from flask_wtf import FlaskForm, Form
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms import validators
from wtforms.fields.core import DateField, FieldList,FormField, IntegerField, SelectField
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
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
    save = SubmitField('Save')
    submit = BooleanField('Submit')
    publish = BooleanField('Publish')


class AuthorForm(FlaskForm):
    """Author SubForm

    Creates the form to add each author
    """
    surname = StringField(
        'Surname',
        render_kw={'placeholder':"Surname"},
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        render_kw={'placeholder':"Email"},

        validators=[DataRequired()]
    )
    firstname = StringField(
        'First Name',
        render_kw={'placeholder':"Name"},

        validators=[DataRequired()]
    )

class ArticleForm(FlaskForm):
    """Form to create the article in the database

    """
    title = StringField(
        'Title',
        render_kw={'placeholder':"Title"},
        validators=[DataRequired()]
    )

    link =  StringField(
        'Link to article',
        render_kw={'placeholder':"Link"},
        validators=[DataRequired()]
    )

    year = IntegerField(
        'Publication Year',
        render_kw={'placeholder':"Year"},
        validators=[DataRequired()]
    )
    
    journal = StringField(
        'Journal',
        render_kw={'placeholder':"Journal"},
        validators=[DataRequired()]
    )
    authors = FieldList(
        FormField(AuthorForm),
        min_entries=1,
        max_entries=20
    )
    submit = SubmitField('Save')
