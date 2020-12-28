from app import db, login_manager
from flask_login import UserMixin

#Login function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Policy-Target Fact-Sheet database
class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', backref='intervention-outcome')

    def __repr__(self):
        """
        This function returns information contained in the sheet
        """
        return f"Fact-Sheet: '{self.title}'"

# Function: getting 3 latest Fact-Sheets
def get_latest(limit: int = 3):
    latest = db.session.query(Sheet.id,
    Sheet.title,
    Sheet.abstract,
    Sheet.picture,).order_by(Sheet.id.desc(),
    ).limit(limit).all()
    return latest


# Source Article Database
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = title = db.Column(db.String(120), unique=True, nullable=False)
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'), nullable=False)

# Contributor Database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    surname = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)



