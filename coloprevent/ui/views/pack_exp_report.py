from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, RadioField, widgets, SubmitField, DateField, IntegerField,TextAreaField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PackShipment, Pack, ExpiryReport
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments


@blueprint.route('/pack_expiry_report', methods=['GET', 'POST'])
def pack_expiry_report():

     q_list = db.session.execute(db.select(ExpiryReport).order_by(ExpiryReport.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)

 
     return render_template('ui/reports/pack_exp_report.html/', ordered_list=ordered_list)



