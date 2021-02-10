import os
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request  # , abort
# from flask_login.utils import login_required # Normally included below, commented to check it works
from app import db, bcrypt
from app.models import Result, Sheet, Contributor, Article, Author
from app.contribution.forms import ArticleForm, AuthorForm, FactSheetForm, ListResultForm, ResultForm
from flask_login import current_user,  login_required
from datetime import date  # For post / update date

contribution = Blueprint('contribution', __name__)


@contribution.route("/contribute", methods=['GET', 'POST'])
@login_required
def contribute():
    usersheet = Contributor.query.filter_by(
        id=current_user.id).first().sheet.all()
    userarticle = Contributor.query.filter_by(
        id=current_user.id).first().article.all()

    return render_template('/contribute.html',
                           usersheets=usersheet,
                           userarticle=userarticle
                           )

# Page to update factsheet


@contribution.route("/contribute/editsheet/<int:fact_id>", methods=['GET', 'POST'])
@login_required
def edit_fact_sheet(fact_id):
    sheet = Article.query.filter_by(id=8).delete()
    db.session.commit()
    sheet = Sheet.query.get_or_404(fact_id)
    # if sheet.author != current_user:
    #     abort(403)
    # Parameters stored in the sheet
    creation = sheet.creation
    title = sheet.policy.lower() + ' on ' + sheet.target.lower()
    target = sheet.target.lower()
    policy = sheet.policy.lower()
    form = FactSheetForm()
    if form.validate_on_submit():
        sheet.title = sheet.title.lower()
        sheet.contributor.append(current_user)
        sheet.abstract = form.abstract.data
        sheet.policy = sheet.policy.lower()
        sheet.target = sheet.target.lower()
        sheet.submit = form.submit.data
        sheet.publish = form.publish.data
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
    return render_template('/edit_fact_sheet.html', form=form,
                           legend="edit",
                           creation=creation,
                           title=title,
                           target=target,
                           policy=policy)


@contribution.route("/contribute/article/new", methods=['GET', 'POST'])
@login_required
def new_article():
    article_form = ArticleForm()
    author_subform = AuthorForm(prefix='authors-_-')
    if article_form.validate_on_submit():
        article = Article(
            creation=date.today(),
            update=date.today(),
            title=article_form.title.data.lower(),
            link=article_form.link.data,
            year=article_form.year.data,
            journal=article_form.journal.data.lower()
        )
        db.session.add(article)
        for author in article_form.authors.data:
            new_author = Author(
                creation=date.today(),
                update=date.today(),
                name=author['firstname'].lower(),
                surname=author['surname'].lower(),
                email=author['email'].lower()
            )
            article.author.append(new_author)
            article.contributor.append(current_user)
        db.session.commit()
        article_id = article.id
        flash('Your Article Sheet has been submitted. Thank you!', 'success')
        return redirect(url_for('contribution.edit_policy_target', article_id=article_id))

    return render_template('/edit_article.html',
                           form=article_form,
                           _template=author_subform
                           )


# Modification of an article
@contribution.route("/contribute/article/edit/<int:article_id>", methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article_db = Article.query.get_or_404(article_id)
    article_form = ArticleForm()
    author_subform = AuthorForm(prefix='authors-_-')
    if article_form.validate_on_submit():
        article_db.creation = article_db.creation
        article_db.update = date.today()
        article_db.title = article_form.title.data.lower()
        article_db.link = str(article_form.link.data)
        article_db.year = article_form.year.data
        article_db.journal = article_form.journal.data.lower()
        authors_form = article_form.authors.data
        authors_db = article_db.author
        # Adding new author
        attributes_forms = [
            [author['firstname'], author['surname'], author['email']]for author in authors_form]
        attributes_db = [[authordb.name, authordb.surname,
                          authordb.email] for authordb in authors_db]
        for attribute in attributes_forms:
            if attribute not in attributes_db:
                new_author = Author(
                    creation=date.today(),
                    update=date.today(),
                    name=attribute[0].lower(),
                    surname=attribute[1].lower(),
                    email=attribute[2].lower()
                )
                article_db.author.append(new_author)
        # Deleting removed author
        for attribute in attributes_db:
            if attribute not in attributes_forms:
                delete_author = Author.query.filter_by(
                    name=attribute[0].lower(), surname=attribute[1].lower(), email=attribute[2].lower()).first()
                article_db.author.remove(delete_author)
        # Appending contributor
        article_db.contributor.append(current_user)
        db.session.commit()
        flash('Your Article has been updated. Thank you!', 'success')
        # return redirect(url_for('contribution.edit_policy_target', article_id = article_id))
    elif request.method == 'GET':
        article_form.title.data = article_db.title.title()
        article_form.link.data = article_db.link
        article_form.journal.data = article_db.journal.title()
        article_form.year.data = article_db.year
        authors = [{'firstname': author.name.title(),
                    'surname': author.surname.title(), 'email': author.email.lower()}
                   for author in article_db.author]
        for author in authors:
            article_form.authors.append_entry(author)

    return render_template('/edit_article.html',
                           form=article_form,
                           _template=author_subform,
                           article_id=article_id
                           )


# Adding policy-target to an article
@contribution.route("/contribute/article/policy-target/<int:article_id>",
                    methods=['GET', 'POST'])
@login_required
def edit_policy_target(article_id):
    article_db = Article.query.get_or_404(article_id)
    result_list = ListResultForm()
    result_subform = ResultForm(prefix='list-_-')
    if result_list.validate_on_submit():
        results_form = result_list.list.data
        results_db = article_db.result
        # Adding new policy-target result
        # Loading the list of policy-targets in the form
        attributes_forms = [[result['policy'], result['policyUnit'],
                             result['target'], result['targetUnit'],
                             result['method'], result['country'],
                             result['year'], result['estimate'],
                             result['standardError'], result['sampleSize']] for result in results_form]
        # Loading the list of policy-targets in the DATABASE for this article
        attributes_db = [[resultdb.policy, resultdb.policyUnit,
                          resultdb.target, resultdb.targetUnit,
                          resultdb.method, resultdb.country,
                          resultdb.yearPolicy, resultdb.estimate,
                          resultdb.standardError, resultdb.sampleSize] for resultdb in results_db]

        for attribute in attributes_forms:
            if attribute not in attributes_db:
                # Checking if the sheet for this policy-target exists
                sheet_name = attribute[0].lower(
                ) + ' on ' + attribute[2].lower()
                sheet = Sheet.query.filter_by(title=sheet_name).first()
                if not sheet:
                    # If it doesn't exist I create it
                    new_sheet = Sheet(
                        creation=date.today(),
                        update=date.today(),
                        title=sheet_name.lower(),
                        policy=attribute[0].lower(),
                        target=attribute[2].lower(),
                        submit=0,
                        publish=0
                    )
                    db.session.add(new_sheet)
                    new_sheet.contributor.append(current_user)
                    db.session.commit()
                    sheet_id = Sheet.query.filter_by(
                        title=sheet_name).first().id
                else:
                    sheet_id = sheet.id

                # Now that I have the sheet id I can create the result entry in db
                new_result = Result(
                    creation=date.today(),
                    update=date.today(),
                    sheet_id=sheet_id,
                    article_id=article_db.id,
                    # Content specific entries
                    policy=attribute[0].lower(),  # policy name
                    policyUnit=attribute[1].upper(),  # policy name
                    target=attribute[2].lower(),  # target name
                    targetUnit=attribute[3].upper(),  # target unit
                    method=attribute[4].upper(),  # identification method
                    country=attribute[5].title(),  # country of study
                    yearPolicy=attribute[6],  # year of programm implementation
                    estimate=float(attribute[7]),  # Point estimate
                    standardError=float(attribute[8]),  # Standard error
                    sampleSize=attribute[9]  # Sample size
                )
                db.session.add(new_result)
        # Deleting removed Result
        for attribute in attributes_db:
            if attribute not in attributes_forms:
                delete_result = Result.query.filter_by(policy=attribute[0].lower(),
                                                       policyUnit=attribute[1].upper(
                ),
                    target=attribute[2].lower(
                ),
                    targetUnit=attribute[3].upper(
                ),
                    method=attribute[4].upper(
                ),
                    country=attribute[5].title(
                ),
                    yearPolicy=attribute[6],
                    estimate=attribute[7],
                    standardError=attribute[8],
                    sampleSize=attribute[9]).first()
                db.session.delete(delete_result)
        # Appending contributor
        article_db.contributor.append(current_user)
        db.session.commit()
        flash('You have succesfully added results to the article. Thank you!', 'success')
        # return redirect(url_for('contribution.contribute'))
    # Charge data to form if already existing
    elif request.method == 'GET':
        results = [{'policy': resultdb.policy.title(),
                    'policyUnit': resultdb.policyUnit.upper(),
                    'target': resultdb.target.title(),
                    'targetUnit': resultdb.targetUnit.upper(),
                    'method': resultdb.method.upper(),
                    'country': resultdb.country.title(),
                    'year': resultdb.yearPolicy,
                    'estimate': resultdb.estimate,
                    'standardError': resultdb.standardError,
                    'sampleSize': resultdb.sampleSize}
                   for resultdb in article_db.result]
        for result in results:
            result_list.list.append_entry(result)

    return render_template('/update_result.html',
                           form=result_list,
                           _template=result_subform,
                           article_id=article_id
                           )
