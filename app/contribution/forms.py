from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms import validators
from wtforms.fields.core import FieldList,FormField, IntegerField
from wtforms.validators import DataRequired, Email #, ValidationError

# Form to edit fact-sheet meta-info
class FactSheetForm(FlaskForm):
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
    save = SubmitField('Save')
    submit = BooleanField('Submit')
    publish = BooleanField('Publish')

# Form to add an author
# Nested into the ArticleForm
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

        validators=[DataRequired(), Email()]
    )
    firstname = StringField(
        'First Name',
        render_kw={'placeholder':"Name"},

        validators=[DataRequired()]
    )

# Form to add an article
# AuthorForm nested into it
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
