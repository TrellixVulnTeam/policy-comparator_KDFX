# App initialisation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1f6cbe23307106cd229b9cfcaea5364'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger' # Class of the message when need to login to access page


from app.contribution.routes import contribution
from app.factsheet.routes import factsheet
from app.main.routes import main
from app.users.routes import users

app.register_blueprint(contribution)
app.register_blueprint(factsheet)
app.register_blueprint(main)
app.register_blueprint(users)