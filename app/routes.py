from sys import path
from flask import render_template, url_for, flash, redirect, request
from flask_login.utils import login_required
import secrets
import os
from app import app, db, bcrypt
from app.models import Sheet, Article, User, get_latest
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, FactSheetForm 
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

# Setting the first page options
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    latest = get_latest()
    return render_template('/index.html',
    latest = latest)

# Information Page
@app.route('/project')
def project():
    return render_template('/project.html')

# Registration Page
@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_paswword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, surname = form.surname.data,
                username = form.username.data, email = form.email.data,
                password = hashed_paswword)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello {form.name.data} {form.surname.data}, you have successfully registered! Thank you, you will soon here from us', 
         'success')
        return redirect(url_for('login'))
    return render_template('/register.html',
    form = form)

# Login Page
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('account'))

        else:
            flash('Login Unsuccessful. Please check email and password and try again!', 'danger')
    return render_template('/login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.surname = form.surname.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    return render_template('/account.html',
    form = form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    output_size = (250*4,175*4)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/contribute/new", methods=['GET','POST'])
@login_required
def new_fact_sheet():
    form = FactSheetForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            sheet = Sheet(title = form.title.data,
                          abstract = form.abstract.data,
                          picture = picture_file)
            db.session.add(sheet)
            db.session.commit()
        else:
            sheet = Sheet(title = form.title.data,
                          abstract = form.abstract.data)
            db.session.add(sheet)
            db.commit()
        flash('Your Policy-Target Fact Sheet has been submitted. Thank you!', 'success')            
        return redirect(url_for('contribute'))

    return render_template('/new_fact_sheet.html', form = form)

@app.route("/contribute", methods=['GET','POST'])
@login_required
def contribute():
    return render_template('/contribute.html')

@app.route('/factsheet/<int:fact_id>')
def sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    return render_template('fact.html', sheet=sheet)