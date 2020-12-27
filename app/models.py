from app import db

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', backref='intervention-outcome')


def get_latest(limit: int = 3):
    latest = db.session.query(Sheet.id,
    Sheet.title,
    Sheet.abstract,
    Sheet.picture,).order_by(Sheet.id.desc(),
    ).limit(limit).all()
    return latest

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = title = db.Column(db.String(120), unique=True, nullable=False)
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'), nullable=False)

