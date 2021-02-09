import os
from flask import Blueprint
from flask import render_template, redirect, url_for
from app import db, bcrypt
from app.models import Sheet
from app.main.forms import MetaAnalysisSelect


factsheet = Blueprint('factsheet', __name__)


@factsheet.route('/factsheet/<int:fact_id>', methods=['GET', 'POST'])
def sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    # Policy/target chosen
    sheet_policy = sheet.policy
    sheet_target = sheet.target

    # Other possible policies
    sheets = Sheet.query.all()
    policies = [sheet.policy for sheet in sheets]
    policies.remove(sheet_policy)
    targets = [sheet.target for sheet in sheets]
    targets.remove(sheet_target)

    # Search Bar Options

    selection = MetaAnalysisSelect()
    selection.policy.choices = [sheet_policy] + policies
    selection.target.choices = [sheet_target] + targets

    if selection.validate_on_submit():
        policy = selection.policy.data
        target = selection.target.data
        name = policy + ' on ' + target

        factsheet = Sheet.query.filter_by(title=name).first()
        return redirect(url_for('factsheet.sheet',
                                fact_id=factsheet.id))

    return render_template('view_fact_sheet.html',
                           sheet=sheet,
                           selection=selection)
