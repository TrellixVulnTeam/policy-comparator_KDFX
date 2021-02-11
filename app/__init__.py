# App initialisation
from logging import makeLogRecord
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from markdown.core import markdown
from app.config import Config
from flask_migrate import Migrate
from flask_pagedown import PageDown
from flask_misaka import Misaka


# Configuration

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
pagedown = PageDown()
markown = Misaka()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# Class of the message when need to login to access page
login_manager.login_message_category = 'danger'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    pagedown.init_app(app)
    markown.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.contribution.routes import contribution
    from app.factsheet.routes import factsheet
    from app.main.routes import main
    from app.users.routes import users

    app.register_blueprint(contribution)
    app.register_blueprint(factsheet)
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
