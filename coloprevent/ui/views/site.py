from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Site
from flask_wtf import FlaskForm

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    q_list = db.session.execute(db.select(Site).order_by(Site.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)
    return render_template('ui/summary.html', ordered_list = ordered_list)
    

class SiteForm(FlaskForm):
    site_name = StringField('Site name', validators=[DataRequired()])
    site_back_up_contact = TextAreaField('Enter back up contact',validators=[DataRequired()])
    site_primary_contact = TextAreaField('Enter Primary contact',validators=[DataRequired()])
    site_code = IntegerField('Site code',validators=[DataRequired()])


@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    site_form = SiteForm()
    if site_form.validate_on_submit():
        site_added = Site(
        site_name= site_form.site_name.data,
        site_back_up_contact = site_form.site_back_up_contact.data,
        site_primary_contact= site_form.site_primary_contact.data,
        site_code = site_form.site_code.data
        )
        db.session.add(site_added)
        db.session.commit()
        return redirect(url_for('ui.index'))
    
    return render_template('ui/add.html', site_form=site_form)

@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Site).where(Site.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.index'))
    return render_template('ui/delete.html', id=id)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Site).where(Site.id == edit_id)).scalar()
        prev_site_name = query_edit.site_name
        prev_site_backup_contact = query_edit.site_backup_contact
        prev_site_primary_contact = query_edit.site_primary_contatct
        prev_site_code = query_edit.site_code

        ed_form=SiteForm(site_name=prev_site_name, site_backup_contact=prev_site_backup_contact, site_primary_contact=prev_site_primary_contact
                         ,site_code=prev_site_code) 

    
    if ed_form.validate_on_submit():
            query_edit.site_name= ed_form.site_name.data
            query_edit.site_backup_contact = ed_form.site_back_up_contact
            query_edit.site_primary_contact = ed_form.site_primary_contact
            query_edit.site_code = ed_form.site_code
            db.session.add(query_edit)
            db.session.commit()
            return redirect(url_for('ui.index'))
        

    return render_template('ui/edit.html', ed_form = ed_form, id=id)