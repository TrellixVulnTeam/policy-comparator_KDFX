from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, ValidationError


class MetaAnalysisSelect(FlaskForm):
    policy = SelectField("policy",
                         render_kw={'placeholder': "--policy--"},
                         choices=["--policy--"],
                         validators=[DataRequired()])
    target = SelectField("target",
                         render_kw={'placeholder': "--target--"},
                         choices=["--target--"],
                         validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_policy(self, policy):
        if policy.data == "--policy--":
            raise ValidationError('Please select a policy')

    def validate_target(self, target):
        if target.data == "--target--":
            raise ValidationError('Please select a target')
