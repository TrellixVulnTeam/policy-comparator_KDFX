import os
from flask import  Blueprint
from flask import render_template
from app import  db, bcrypt
from app.models import Sheet


factsheet = Blueprint('factsheet', __name__)


@factsheet.route('/factsheet/<int:fact_id>')
def sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    return render_template('view_fact_sheet.html', sheet=sheet)
