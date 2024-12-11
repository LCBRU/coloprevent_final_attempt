from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, RadioField, widgets
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Site
from flask_wtf import FlaskForm

class PacktypeForm(FlaskForm):
    pack_type_name = RadioField(u'Packtypes',choices=[('screening', 'Screening'), ('fit', 'FIT'), ('research', 'Research'), ('tissue_ffpe', 'Tissue/FFPE')])

@blueprint.route('/packtypes', methods=['GET', 'POST'])
def packtypes_home():
     packtypes_form = PacktypeForm()
     return render_template('ui/packtypes/packtypes_home.html',packtypes_form=packtypes_form)


