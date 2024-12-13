from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, RadioField, widgets, SubmitField, DateField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PackShipments
from flask_wtf import FlaskForm

class ShipmentForm(FlaskForm):
    pack_identity = StringField(label="Pack Id", validators=[DataRequired()])
    pack_expiry = DateField(format='%Y-%m-%d')
    addressee =StringField(label="Addressee", validators=[DataRequired()])
    date_posted = DateField(format='%Y-%m-%d')
    date_received = DateField(format='%Y-%m-%d')
    next_due = DateField(format='%Y-%m-%d')
    submit = SubmitField()

@blueprint.route('/packtypes', methods=['GET', 'POST'])
def add_shipments():
     shipment_form = ShipmentForm()
     if shipment_form.validate_on_submit():
        pack_added = PackShipments(
        name= shipment_form.pack_type_name.data  #need to change and create the form 
        )
        db.session.add(pack_added)
        db.session.commit()
        return redirect(url_for('ui.packtypes_home'))

     return render_template('ui/packtypes/add_packtypes.html',shipment_form=shipment_form)