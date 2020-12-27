from flask import render_template, url_for, flash, redirect
from app import app
from app.models import Sheet, Article, get_latest
from app.forms import RegistrationForm, LoginForm

# Setting the first page options
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('/index.html',
    latest = get_latest())

# Information Page
@app.route('/project')
def project():
    return render_template('/project.html')

# Registration Page
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Hello {form.name.data} {form.surname.data}, you have successfully registered! Thank you, you will soon here from us', 'success')
        return redirect(url_for('index'))
    return render_template('/register.html',
    form = form)

# Login Page
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'test': #Just for testing
            flash('Hello, you have successfully logged in! Thank you for your contribution.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please try again!', 'danger')
    return render_template('/login.html', form=form)