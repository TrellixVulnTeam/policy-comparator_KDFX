# App initialisation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1f6cbe23307106cd229b9cfcaea5364'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

from app import routes