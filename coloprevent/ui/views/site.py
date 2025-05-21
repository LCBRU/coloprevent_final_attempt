from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select, cast, func, Integer
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Site
from flask_wtf import FlaskForm
@blueprint.route('/site_home', methods=['GET', 'POST'])
def site_home():
    search_form = SearchForm(search_placeholder='Search site name', formdata=request.args) 
    q = db.select(Site).order_by(
    cast(
        func.substr(Site.site_name, func.instr(Site.site_name, ' ') + 1), Integer
    ),
    func.substr(Site.site_name, func.char_length(Site.site_name) - 1, 1)
)




    if search_form.search.data:
        q = q.where(Site.site_name.like(f'%{search_form.search.data}%'))
    q_list = db.session.execute(q).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    
    return render_template('ui/summary.html', ordered_list = ordered_list, search_form=search_form)
    

class SiteForm(FlashingForm):
    site_name = StringField('Site name', validators=[DataRequired()])
    site_primary_contact = TextAreaField('Primary contact',validators=[DataRequired()])
    site_backup_contact = TextAreaField('Back up contact',validators=[DataRequired()])
    site_code = StringField('Site code',validators=[DataRequired()])


@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    site_form = SiteForm()
    if site_form.validate_on_submit():
        site_added = Site(
        site_name= site_form.site_name.data,
        site_backup_contact = site_form.site_backup_contact.data,
        site_primary_contact= site_form.site_primary_contact.data,
        site_code = site_form.site_code.data
        )
        db.session.add(site_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=site_form, title="Add Site", url=url_for("ui.add"))

@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Site).where(Site.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.site_home'))
    return render_template('ui/delete.html', id=id)


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Site).where(Site.id == edit_id)).scalar()
        prev_site_name = query_edit.site_name
        prev_site_backup_contact = query_edit.site_backup_contact
        prev_site_primary_contact = query_edit.site_primary_contact
        prev_site_code = query_edit.site_code

        ed_form=SiteForm(site_name=prev_site_name, site_backup_contact=prev_site_backup_contact, site_primary_contact=prev_site_primary_contact
                         ,site_code=prev_site_code) 

    
    if ed_form.validate_on_submit():
            query_edit.site_name= ed_form.site_name.data
            query_edit.site_backup_contact = ed_form.site_backup_contact.data
            query_edit.site_primary_contact = ed_form.site_primary_contact.data
            query_edit.site_code = ed_form.site_code.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Site", url=url_for("ui.edit",id=id))