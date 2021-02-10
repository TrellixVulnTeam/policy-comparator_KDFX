import os
from flask import Blueprint
from flask import render_template, redirect, url_for, request
from app import db, bcrypt
from app.models import Sheet
from app.factsheet.utils import url_sheet, policy_target_from_url
from app.main.forms import MetaAnalysisSelect
from app.main.utils import remove_duplicates


factsheet = Blueprint('factsheet', __name__)


@factsheet.route('/factsheet/<link>', methods=['GET', 'POST'])
def sheet(link):
    policy, target = policy_target_from_url(link)
    id = Sheet.query.filter_by(policy=policy,
                               target=target).first().id
    sheet = Sheet.query.get_or_404(id)

    # Policy/target chosen
    sheet_policy = sheet.policy
    sheet_target = sheet.target

    # Other possible policies
    sheets = Sheet.query.filter_by(publish=True).all()
    policies = remove_duplicates([sheet.policy.title() for sheet in sheets])
    policies.remove(sheet_policy.title())
    targets = remove_duplicates([sheet.target.title() for sheet in sheets])
    targets.remove(sheet_target.title())

    # Search Bar Options

    selection = MetaAnalysisSelect()
    selection.policy.choices = [sheet_policy.title()] + policies
    selection.target.choices = [sheet_target.title()] + targets

    if selection.validate_on_submit():
        policy = selection.policy.data.lower()
        target = selection.target.data.lower()
        name = policy + ' on ' + target

        factsheet = Sheet.query.filter_by(title=name).first()
        return redirect(url_for('factsheet.sheet',
                                link=url_sheet(factsheet.id)))

    return render_template('view_fact_sheet.html',
                           sheet=sheet,
                           selection=selection)
