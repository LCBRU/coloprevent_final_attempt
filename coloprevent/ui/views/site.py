from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Site

@blueprint.route('/site_home', methods=['GET', 'POST'])
def site_home():
    search_form = SearchForm(search_placeholder='Search site name', formdata=request.args) 
    q = db.select(Site).order_by(Site.site_name)

    if search_form.search.data:
        q = q.where(Site.site_name.like(f'%{search_form.search.data}%'))

    sites = db.paginate(select=q)

    return render_template('ui/summary.html', search_form=search_form, sites=sites)
    

class SiteForm(FlashingForm):
    site_name = StringField('Site name', validators=[DataRequired(), Length(max=100)])
    site_primary_contact = TextAreaField('Primary contact',validators=[DataRequired()])
    site_backup_contact = TextAreaField('Back up contact',validators=[DataRequired()])
    site_code = StringField('Site code',validators=[DataRequired(), Length(max=100)])


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

@blueprint.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = db.session.get(Site, id)

    if item is not None:
        db.session.delete(item)
        db.session.commit()

    return refresh_response()


@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        site = db.session.execute(db.select(Site).where(Site.id == edit_id)).scalar()
        ed_form = SiteForm(obj=site)
    
    if ed_form.validate_on_submit():
        site.site_name= ed_form.site_name.data
        site.site_backup_contact = ed_form.site_backup_contact.data
        site.site_primary_contact = ed_form.site_primary_contact.data
        site.site_code = ed_form.site_code.data
        db.session.add(site)
        db.session.commit()
        return refresh_response()
        
    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Site", url=url_for("ui.edit",id=id))