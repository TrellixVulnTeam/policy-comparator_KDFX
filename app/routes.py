from sys import path
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login.utils import login_required
import secrets
import os
from app import app, db, bcrypt
from app.models import Sheet, Contributor, Article, Author, Result, get_latest
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
        contributor = Contributor(name = form.name.data, surname = form.surname.data,
         email = form.email.data,
                password = hashed_paswword)
        db.session.add(contributor)
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
        contributor = Contributor.query.filter_by(email = form.email.data).first()
        if contributor and bcrypt.check_password_hash(contributor.password, form.password.data):
            login_user(contributor, remember=form.remember.data)
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

# Account page
@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.surname = form.surname.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    return render_template('/account.html',
    form = form)

# Saving picture function
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    output_size = (250*4,175*4) #Size of the picture
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
    usersheet = Contributor.query.filter_by(id = current_user.id).first().sheet.all()
    return render_template('/contribute.html', 
    usersheets=usersheet
    )

@app.route('/factsheet/<int:fact_id>')
def sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    return render_template('fact.html', sheet=sheet)

# Page to update factsheet
@app.route("/contribute/<int:fact_id>/update")
@login_required
def update_fact_sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    if sheet.author != current_user:
        abort(403)
    form = FactSheetForm()
    return render_template('/new_fact_sheet.html', form = form)