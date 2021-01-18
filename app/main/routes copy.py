from sys import path, prefix
from flask import current_app, render_template, url_for, flash, redirect, request, abort
from flask_login.utils import login_required
import secrets
import os
from app import db, bcrypt
from app.models import Sheet, Contributor, Article, Author, Result, get_latest
from app.forms import ArticleForm, AuthorForm, RegistrationForm, LoginForm, UpdateAccountForm, FactSheetForm 
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from datetime import date # For post / update date
from jinja2 import Template
