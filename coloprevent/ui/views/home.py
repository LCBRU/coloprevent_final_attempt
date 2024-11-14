from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField
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
    return render_template('ui/summary.html', order_list = ordered_list)
    

class SiteForm(FlaskForm):
    site_name = StringField('name', validators=[DataRequired()])


@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    site_form = SiteForm()
    if site_form.validate_on_submit():
        site_added = Site(
        name_of_site= site_form.site_name.data
        )
        db.session.add(site_added)
        db.session.commit()
        return redirect(url_for('summary'))
    
    return render_template('ui/add.html')

@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Site).where(Site.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect("/summary")
    return render_template('delete.html', id=id)

def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Site).where(Site.id == edit_id)).scalar()
        prev_site_name = query_edit.site_name
        ed_form=SiteForm(site_name=prev_site_name) 

    
    if ed_form.validate_on_submit():
            query_edit.site_name= ed_form.site_name.data
            db.session.add(query_edit)
            db.session.commit()
            return redirect("/summary")
        

    return render_template('edit.html', ed_form = ed_form, id=id)