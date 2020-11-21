# App initialisation
from flask import Flask, render_template

app = Flask(__name__)


# Setting the first page options
@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')

# Information Page
@app.route('/project')
def project():
    return render_template('/project.html')


# Generating the website
if __name__=='__main__':
    app.run()
