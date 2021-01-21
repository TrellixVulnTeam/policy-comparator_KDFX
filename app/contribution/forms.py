from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms import validators
from wtforms.fields.core import FieldList,FormField, IntegerField
from wtforms.validators import DataRequired, Email, Regexp #, ValidationError

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
    submit = SubmitField('Save and go to Article Results')


# Form to add a policy-target to an article
# Nested into ListResultForm
class ResultForm(FlaskForm):
    """Form to create the policy-target
    """
    policy = StringField(
        'Policy',
        render_kw={'placeholder':"Policy"},
        validators=[DataRequired()]
    )
    target = StringField(
        'Target',
        render_kw={'placeholder':"Target"},
        validators=[DataRequired()]
    )
    policyUnit = StringField(
        'Policy Unit',
        render_kw={'placeholder':"Policy Unit"},
        validators=[DataRequired()]
    )
    targetUnit = StringField(
        'Policy Unit',
        render_kw={'placeholder':"Policy Unit"},
        validators=[DataRequired()]
    )
    method = StringField(
        'Identification Method',
        render_kw={'placeholder':"Identification Method"},
        validators=[DataRequired()]
    )
    country = StringField(
        'Program Country',
        render_kw={'placeholder':"Program Country"},
        validators=[DataRequired()]
    )
    year = IntegerField(
        'Program Year',
        render_kw={'placeholder':"Program Year"},
        validators=[DataRequired()]
    )
    estimate = FloatField(
        'Estimate',
        render_kw={'placeholder':"Estimate"},
        validators=[DataRequired()]
    )
    standardError = FloatField(
        'Standard-Error',
        render_kw={'placeholder':"Standard-Error"},
        validators=[DataRequired()]
    )
    
    sampleSize = IntegerField(
        'Sample Size',
        render_kw={'placeholder':"Sample Size"},
        validators=[DataRequired()]
    )

class ListResultForm(FlaskForm):
    """Form to submit list of policy-targets to database

    """
    list = FieldList(
        FormField(ResultForm),
        min_entries=1,
        max_entries=20
    )
    submit = SubmitField('Save and go back to contributor menu')
