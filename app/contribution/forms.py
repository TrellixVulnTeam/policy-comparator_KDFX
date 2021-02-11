from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms import validators
from wtforms.fields.core import FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Email, URL  # , ValidationError
from flask_pagedown.fields import PageDownField

# Edit page


class PageForm(FlaskForm):
    title = StringField('Page name',
                        validators=[DataRequired()])
    text = PageDownField('Enter the page markdown')
    submit = SubmitField('Save')

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
        render_kw={'placeholder': "Enter the author surname"},
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        render_kw={'placeholder': "Enter the author email"},

        validators=[DataRequired(), Email()]
    )
    firstname = StringField(
        'First Name',
        render_kw={'placeholder': "Enter the author's first name"},

        validators=[DataRequired()]
    )

# Form to add an article
# AuthorForm nested into it


class ArticleForm(FlaskForm):
    """Form to create the article in the database

    """
    title = StringField(
        'Article Title',
        render_kw={'placeholder': "Enter the article title"},
        validators=[DataRequired()]
    )

    link = StringField(
        'Article link',
        render_kw={'placeholder': "Enter the article link"},
        validators=[DataRequired(), URL(message='Must be a valid URL')]
    )

    year = IntegerField(
        'Publication Year',
        render_kw={'placeholder': "Enter the publication year of the article"},
        validators=[DataRequired()]
    )

    journal = StringField(
        'Journal',
        render_kw={'placeholder': "Journal in which the article was published"},
        validators=[DataRequired()]
    )
    authors = FieldList(
        FormField(AuthorForm),
        min_entries=1,
        max_entries=20
    )
    submit = SubmitField('Save General Informations')


# Form to add a policy-target to an article
# Nested into ListResultForm
class ResultForm(FlaskForm):
    """Form to create the policy-target
    """
    policy = StringField(
        'Policy',
        render_kw={'placeholder': "Enter or select the type of intervention"},
        validators=[DataRequired()]
    )
    target = StringField(
        'Target',
        render_kw={'placeholder': "Enter or select the target measure"},
        validators=[DataRequired()]
    )
    policyUnit = StringField(
        'Policy unit',
        render_kw={
            'placeholder': "Enter or select the policy unit of measurement"},
        validators=[DataRequired()]
    )
    targetUnit = StringField(
        'Target unit',
        render_kw={
            'placeholder': "Enter or select the target unit of measurement"},
        validators=[DataRequired()]
    )
    method = StringField(
        'Identification Method',
        render_kw={'placeholder': "Enter or select the identification strategy"},
        validators=[DataRequired()]
    )
    country = StringField(
        'Program Country',
        render_kw={
            'placeholder': "Select the country in which the program took place"},
        validators=[DataRequired()]
    )
    year = IntegerField(
        'Program Year',
        render_kw={'placeholder': "Select the year the program took place"},
        validators=[DataRequired()]
    )
    estimate = FloatField(
        'Estimate',
        render_kw={
            'placeholder': "Copy the causal effect of the policy on the target from article"},
        validators=[DataRequired()]
    )
    standardError = FloatField(
        'Standard-Error',
        render_kw={'placeholder': "Copy the associated standard-error"},
        validators=[DataRequired()]
    )

    sampleSize = IntegerField(
        'Sample Size',
        render_kw={'placeholder': "Copy the sample size"},
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
    submit = SubmitField('Save Results')
