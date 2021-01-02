# Testing zone
from app import db
db.create_all()

from app.models import Sheet, Contributor, Article, Author, Result
from datetime import date


contributor1 = Contributor(name="Yann",
surname="David",email="yann.collindavid@gmail.com",
password =  "test123")

db.session.add(contributor1)

contributor2= Contributor(name="Gael",
surname="David",email="gdavid44@gmail.com",
password =  "test123")


db.session.add(contributor2)

db.session.commit()

# Contributor.query.first().password
contributor1 = Contributor.query.first()


sheet1 = Sheet(creation = date.today(),
update = date.today(),title = "First Sheet",
abstract = "This is the very first sheet",
policy ="Carbon Tax",
target = "CO2 Emissions",
submit = False,
publish=False)


sheet1.contributor.append(contributor1)
db.session.commit()

Sheet.query.first().contributor

author1=Author(creation = date.today(), # Date of entry creation in database
    update = date.today(), # Date of entry update in database
    # Content specific entries
    surname = "BigFlo", 
    name = "Esther",
    email = "bigflo@mail.com")

db.session.add(author1)

author2=Author(creation = date.today(), # Date of entry creation in database
    update = date.today(), # Date of entry update in database
    # Content specific entries
    surname = "Doe", 
    name = "John",
    email = "johndoe@mail.com")

db.session.add(author1)

db.session.add(author2)


article1 = Article(
    creation = date.today(), # Date of entry creation in database
    update = date.today(), # Date of entry update in database

    # Content specific entries
    title = "The Importance of Being Earnest", #article title
    link =  "test.com", #link to article
    year = 2013, # year of publication
    journal = "Journal of Testing"
    # Many-to-many relation created with authors above
    # Many-to-many relation created with contributors above
)
db.session.add(article1)
db.session.commit()

article1.contributor.append(contributor1)

result1 = Result(
    creation = date.today(), # Date of entry creation in database
    update = date.today(), # Date of entry update in database
    # Content specific entries
    policy = "Carbon Tax",
    target = "CO2 Emissions" ,# target name
    method = "RCT", # identification method
    country = "France", # country of study
    yearPolicy = 2011, # year of programm implementation
    estimate = 3.2, # Point estimate
    standardError = 0.96, # Standard error
    sampleSize = 2000 # Sample size
)

result1.contributor.append(contributor1)

result2 = Result(
    creation = date.today(), # Date of entry creation in database
    update = date.today(), # Date of entry update in database
    

    # Content specific entries
    policy = "Carbon Tax",
    target = "CO2 Emissions" ,# target name
    method = "RCT", # identification method
    country = "France", # country of study
    yearPolicy = 2011, # year of programm implementation
    estimate = 3.8, # Point estimate
    standardError = 1.4, # Standard error
    sampleSize = 1500 # Sample size
)
result2.contributor.append(contributor1)

db.session.add(result1)
db.session.add(result2)
db.session.commit()


Article.query.filter_by(title="The Importance of Being Earnest").first().author.append(author1) 

db.session.commit()
yann = Contributor.query.filter_by(name="Yann").first()
yann.sheet.all()

article1 = Article.query.first()

sheet1 = Sheet.query.first()
sheet1.policy + ' on ' + sheet1.target
sheet1.contributor.append(yann)
db.session.commit()