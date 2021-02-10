import os
from flask import Blueprint, jsonify, render_template, url_for, redirect
from flask.globals import request
from flask.helpers import flash
from app import db, bcrypt
from app.models import Sheet
from app.main.forms import MetaAnalysisSelect
from app.factsheet.utils import url_sheet
from app.main.utils import remove_duplicates

main = Blueprint('main', __name__)

# Search bar function


# Setting the first page options
@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    sheets = Sheet.query.filter_by(publish=True).all()
    selection = MetaAnalysisSelect()
    # Only take unique values
    selection.policy.choices += remove_duplicates(
        [sheet.policy.title() for sheet in sheets])
    selection.target.choices += remove_duplicates(
        [sheet.target.title() for sheet in sheets])

    if selection.validate_on_submit():
        policy = selection.policy.data.lower()
        target = selection.target.data.lower()
        name = policy + ' on ' + target

        factsheet = Sheet.query.filter_by(title=name).first()
        return redirect(url_for('factsheet.sheet',
                                link=url_sheet(factsheet.id)))

    return render_template('/index.html',
                           selection=selection)

# Information Page

# For development of future possibilities
# @main.route('/policy/<target>')
# def policy(target):
#     policies = Sheet.query.filter_by(target=target).all()
#     policyObj = [policy.policy for policy in policies]

#     return jsonify({'policies': policyObj})


@ main.route('/target/<policy>')
def target(policy):
    targets = Sheet.query.filter_by(policy=policy,
                                    publish=True).all()
    targetObj = [target.target.title() for target in targets]

    return jsonify({'targets': targetObj})


@ main.route('/project', methods=['GET', 'POST'])
def project():
    sheets = Sheet.query.filter_by(publish=True).all()
    selection = MetaAnalysisSelect()
    # Set option specified to have unique value of each policy/target
    selection.policy.choices += remove_duplicates(
        [sheet.policy.title() for sheet in sheets])
    selection.target.choices += remove_duplicates(
        [sheet.target.title() for sheet in sheets])

    if selection.validate_on_submit():
        policy = selection.policy.data.lower()
        target = selection.target.data.lower()
        name = policy + ' on ' + target

        factsheet = Sheet.query.filter_by(title=name).first()
        return redirect(url_for('factsheet.sheet',
                                link=url_sheet(factsheet.id)))
    return render_template('/project.html', selection=selection)
