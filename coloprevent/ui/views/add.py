from .. import blueprint
from flask import render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from coloprevent.model import Site
from lbrc_flask.database import db
import os


#'blueprint.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

class SiteForm(FlaskForm):
    site_name = StringField('name', validators=[DataRequired()])


@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    site_form = SiteForm
    if site_form.validate_on_submit():
        site_added = Site(
        name_of_site= site_form.site_name.data
        )
        db.session.add(site_added)
        db.session.commit()
        return redirect(url_for('summary'))
    
    return render_template('ui/add.html')