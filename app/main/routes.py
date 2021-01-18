import os
from flask import Blueprint
from flask import render_template
from app import app, db, bcrypt
from app.models import get_latest

main = Blueprint('main', __name__)


# Setting the first page options
@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    latest = get_latest()
    return render_template('/index.html',
    latest = latest)

# Information Page
@main.route('/project')
def project():
    return render_template('/project.html')

