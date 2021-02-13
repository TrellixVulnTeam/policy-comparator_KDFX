from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import Column
from app import db, login_manager
from flask_login import UserMixin
# A. Login function


@login_manager.user_loader
def load_user(user_id):
    return Contributor.query.get(int(user_id))


# B. Functions creating the many-to-many relational tables
# B.1. Relation between contributor and sheet
contributor_sheet = db.Table('contributorSheet',
                             db.Column('contributor_id', db.Integer,
                                       db.ForeignKey('contributor.id')),
                             db.Column('sheet_id', db.Integer,
                                       db.ForeignKey('sheet.id')),
                             )

# B.2. Relation between contributor and article
contributor_article = db.Table('contributorArticle',
                               db.Column('contributor_id', db.Integer,
                                         db.ForeignKey('contributor.id')),
                               db.Column('article_id', db.Integer,
                                         db.ForeignKey('article.id')),
                               )

# B.3. Relation between contributor and result
contributor_result = db.Table('contributorResult',
                              db.Column('contributor_id', db.Integer,
                                        db.ForeignKey('contributor.id')),
                              db.Column('result_id', db.Integer,
                                        db.ForeignKey('result.id')),
                              )

# B.4. Relation between article and author
article_author = db.Table('articleAuthor',
                          db.Column('article_id', db.Integer,
                                    db.ForeignKey('article.id')),
                          db.Column('author_id', db.Integer,
                                    db.ForeignKey('author.id')),
                          )


# C. Creation of the databases

# C.1. Contributor Database


class Contributor(db.Model, UserMixin):
    __tablename__ = 'contributor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    access = db.Column(db.String,  nullable=False, default='contributor')
    # Creation of the relation between contributors and sheets
    sheet = db.relationship('Sheet', secondary=contributor_sheet,
                            backref=db.backref('contributor'),
                            lazy='dynamic')
    article = db.relationship('Article', secondary=contributor_article,
                              backref=db.backref('contributor'),
                              lazy='dynamic')
    result = db.relationship('Result', secondary=contributor_result,
                             backref=db.backref('contributor'),
                             lazy='dynamic')

    def __repr__(self):
        """
        This function returns information contained in the sheet
        """
        return f"Contributor: {self.name} {self.surname}"

# Fact sheet


class Sheet(db.Model):
    __tablename__ = 'sheet'
    # Tool specific entries
    id = db.Column(db.Integer, primary_key=True)
    # Date of entry creation in database
    creation = db.Column(db.Date, nullable=False)
    # Date of entry update in database
    update = db.Column(db.Date, nullable=False)
    # Many-to-many relation created with contributors above

    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.Text, nullable=False,
                         default="This sheet has not been edited")
    # picture = db.Column(db.String, nullable=False)
    policy = db.Column(db.String, nullable=False)
    target = db.Column(db.String, nullable=False)
    # O-t-m relation with results
    result = db.relationship('Result', backref='sheet')
    submit = db.Column(db.Boolean, nullable=False, default=False)
    publish = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """
        This function returns information contained in the sheet
        """
        return f"Fact-Sheet: '{self.title}'"


# Function to retrieve the last three fact-sheets for home page


def get_latest(limit: int = 3):
    latest = db.session.query(Sheet.id,
                              Sheet.title,
                              Sheet.abstract
                              # , Sheet.picture,
                              ).order_by(Sheet.id.desc(),
                                         ).filter_by(publish=True).limit(limit).all()
    return latest


# C.3. Source Article Database
class Article(db.Model):
    __tablename__ = 'article'
    # Tool specific entries
    id = db.Column(db.Integer, primary_key=True)
    # Date of entry creation in database
    creation = db.Column(db.Date, nullable=False)
    # Date of entry update in database
    update = db.Column(db.Date, nullable=False)
    # Contributor

    # Content specific entries
    title = db.Column(db.String(120), unique=True,
                      nullable=False)  # article title
    link = db.Column(db.String, unique=True, nullable=False)  # link to article
    year = db.Column(db.Integer, nullable=False)  # year of publication
    journal = db.Column(db.String, unique=False, nullable=False)
    # Many-to-many relation created with authors above
    # Many-to-many relation created with contributors above
    # O-t-m relation with results
    result = db.relationship('Result', backref='article')


# C.4. Authors database
class Author(db.Model):
    __tablename__ = 'author'
    # Tool specific entries
    id = db.Column(db.Integer, primary_key=True)
    # Date of entry creation in database
    creation = db.Column(db.Date, nullable=False)
    # Date of entry update in database
    update = db.Column(db.Date, nullable=False)

    # Content specific entries
    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    # Creates a many-to-many relationship between authors and articles
    article = db.relationship('Article', secondary=article_author,
                              backref=db.backref('author'),
                              lazy='dynamic')

# C.5. Results database


class Result(db.Model):
    __tablename__ = 'result'
    # Tool specific entries
    id = db.Column(db.Integer, primary_key=True)
    # Date of entry creation in database
    creation = db.Column(db.Date, nullable=False)
    # Date of entry update in database
    update = db.Column(db.Date, nullable=False)
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    # Many-to-many relation created with contributors above

    # Content specific entries
    policy = db.Column(db.String, nullable=False)  # policy name
    target = db.Column(db.String, nullable=False)  # target name
    policyUnit = db.Column(db.String, nullable=True,
                           default="TBD")  # policy unit
    targetUnit = db.Column(db.String, nullable=True,
                           default="TBD")  # target unit
    method = db.Column(db.String, nullable=False)  # identification method
    country = db.Column(db.String, nullable=False)  # country of study
    # year of programm implementation
    yearPolicy = db.Column(db.Integer, nullable=False)
    estimate = db.Column(db.Float, nullable=False)  # Point estimate
    standardError = db.Column(db.Float, nullable=False)  # Standard error
    sampleSize = db.Column(db.Integer, nullable=False)  # Sample size

# Pages tables


class Pages(db.Model):
    __tablename__ = 'pages'
    # Tool specific entries
    id = db.Column(db.Integer, primary_key=True)
    # Date of entry creation in database
    text = db.Column(db.Text, nullable=False)
    page = db.Column(db.String, nullable=False)
    rank = db.Column(db.Integer, nullable=True)
