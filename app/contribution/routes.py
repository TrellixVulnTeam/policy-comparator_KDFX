import os
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request#, abort
# from flask_login.utils import login_required # Normally included below, commented to check it works
from app import db, bcrypt
from app.models import Sheet, Contributor, Article, Author
from app.contribution.forms import ArticleForm, AuthorForm, FactSheetForm 
from flask_login import  current_user,  login_required
from datetime import date # For post / update date

contribution = Blueprint('contribution', __name__)



@contribution.route("/contribute", methods=['GET','POST'])
@login_required
def contribute():
    usersheet = Contributor.query.filter_by(id = current_user.id).first().sheet.all()
    userarticle = Contributor.query.filter_by(id = current_user.id).first().article.all()

    return render_template('/contribute.html', 
    usersheets=usersheet,
    userarticle = userarticle
    )

# Page to update factsheet
@contribution.route("/contribute/editsheet/<int:fact_id>", methods=['GET','POST'])
@login_required
def edit_fact_sheet(fact_id):
    sheet = Sheet.query.get_or_404(fact_id)
    # if sheet.author != current_user:
    #     abort(403)
    # Parameters stored in the sheet
    creation = sheet.creation
    title = sheet.policy + ' on ' + sheet.target
    target = sheet.target
    policy = sheet.policy
    form = FactSheetForm()
    if form.validate_on_submit():
        sheet.title = sheet.title
        sheet.contributor.append(current_user)
        sheet.abstract = form.abstract.data
        sheet.policy = sheet.policy
        sheet.target = sheet.target
        sheet.submit = form.submit.data
        sheet.publish= form.publish.data
        if creation:
            sheet.creation = sheet.creation
        else:
            sheet.creation = date.today()
        db.session.commit()
        flash('Your Policy-Target Sheet has been submitted. Thank you!', 'success') 
                   
        return redirect(url_for('contribution.contribute'))

    elif request.method == 'GET':
        form.abstract.data = sheet.abstract
        form.submit.data = sheet.submit
        form.publish.data = sheet.publish    
    return render_template('/fact_sheet.html', form = form,
                            legend = "edit",
                            creation = creation,
                            title = title,
                            target = target,
                            policy = policy )


@contribution.route("/contribute/newarticle", methods=['GET','POST'])
@login_required
def new_article():
    article_form = ArticleForm()
    author_subform = AuthorForm(prefix='authors-_-')
    if article_form.validate_on_submit():
        article = Article(
            creation = date.today(),
            update = date.today(),
            title = article_form.title.data,
            link = article_form.link.data,
            year = article_form.year.data,
            journal = article_form.journal.data
        )
        db.session.add(article)
        for author in article_form.authors.data:
            new_author = Author(
                creation = date.today(),
                update = date.today(),
                name = author['firstname'],
                surname = author['surname'],
                email = author['email']
            )
            article.author.append(new_author)
            article.contributor.append(current_user)
        db.session.commit()   
        flash('Your Article Sheet has been submitted. Thank you!', 'success')            
        return redirect(url_for('contribution.contribute'))

    return render_template('/new_article.html',
            form = article_form,
            _template = author_subform
    )

@contribution.route("/contribute/editarticle/<int:article_id>", methods=['GET','POST'])
@login_required
def edit_article(article_id):
    article_db = Article.query.get_or_404(article_id)
    article_form = ArticleForm()
    author_subform = AuthorForm(prefix='authors-_-')
    if article_form.validate_on_submit():
        article_db.creation = article_db.creation
        article_db.update = date.today()
        article_db.title = article_form.title.data
        article_db.link = article_form.link.data
        article_db.year = article_form.year.data
        article_db.journal = article_form.journal.data
        authors_form =  article_form.authors.data
        authors_db = article_db.author
        # Adding new author
        attributes_forms = [[author['firstname'], author['surname'],author['email']]for author in authors_form]
        attributes_db = [[authordb.name, authordb.surname,authordb.email] for authordb in authors_db ]
        for attribute in attributes_forms:
            if attribute not in attributes_db:
                    new_author = Author(
                        creation = date.today(),
                        update = date.today(),
                        name = attribute[0],
                        surname = attribute[1],
                        email = attribute[2]
                    )
                    article_db.author.append(new_author)
        # Deleting reoved author
        for attribute in attributes_db:
            if attribute not in attributes_forms:
                delete_author = Author.query.filter_by(name = attribute[0], surname=attribute[1], email=attribute[2]).first()
                article_db.author.remove(delete_author)
        # Appending contributor
        article_db.contributor.append(current_user)
        db.session.commit()   
        flash('Your Article Sheet has been updated. Thank you!', 'success')            
        return redirect(url_for('contribution.contribute'))
    elif request.method == 'GET':
        article_form.title.data = article_db.title
        article_form.link.data = article_db.link
        article_form.journal.data = article_db.journal
        article_form.year.data = article_db.year
        authors = [{'firstname': author.name, 'surname':author.surname, 'email':author.email} 
                    for author in article_db.author]
        for author in authors:
            article_form.authors.append_entry(author)

    return render_template('/new_article.html',
            form = article_form,
            _template = author_subform
    )