import os
from re import template
from flask import current_app, Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login.utils import login_required, logout_user, login_user
from app import db, bcrypt
from app.models import Contributor
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import current_user
from datetime import date  # For post / update date
from jinja2 import Template
from app.users.utils import admin_required
users = Blueprint('users', __name__)


# Registration Page
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_paswword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        contributor = Contributor(name=form.name.data, surname=form.surname.data,
                                  email=form.email.data, password=hashed_paswword,
                                  access='admin')
        db.session.add(contributor)
        db.session.commit()
        flash(f'Hello {form.name.data} {form.surname.data}, you have successfully registered! Thank you, you will soon here from us',
              'success')
        return redirect(url_for('users.login'))
    return render_template('/register.html',
                           form=form)

# Login Page


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        contributor = Contributor.query.filter_by(
            email=form.email.data).first()
        if contributor and bcrypt.check_password_hash(contributor.password, form.password.data):
            login_user(contributor, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('contribution.contribute'))

        else:
            flash(
                'Login Unsuccessful. Please check email and password and try again!', 'danger')
    return render_template('/login.html', form=form)


@users.route("/contributors")
@admin_required
def contributors():
    users = Contributor.query.all()
    return render_template("/contributors.html", users=users)


@users.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('main.index'))

# Account page


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.surname = form.surname.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    return render_template('/account.html',
                           form=form)
