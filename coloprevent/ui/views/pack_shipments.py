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


@blueprint.route('/shipments', methods=['GET', 'POST'])
def shipment_home():
     q_list = db.session.execute(db.select(PackShipments).order_by(PackShipments.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)
 
     return render_template('ui/pack_shipments/pack_shipments_home.html', ordered_list=ordered_list)



class ShipmentForm(FlaskForm):
    pack_identity = StringField(label="Pack Id", validators=[DataRequired()])
    pack_expiry = DateField(format='%Y-%m-%d')
    addressee =StringField(label="Addressee", validators=[DataRequired()])
    date_posted = DateField(format='%Y-%m-%d')
    date_received = DateField(format='%Y-%m-%d')
    next_due = DateField(format='%Y-%m-%d')
    submit = SubmitField()

@blueprint.route('/add_shipments', methods=['GET', 'POST'])
def add_shipments():
     shipment_form = ShipmentForm()
     if shipment_form.validate_on_submit():
        pack_added = PackShipments(
        pack_ids= shipment_form.pack_identity.data,
        pack_expiry= shipment_form.pack_expiry.data,
        addressee= shipment_form.addressee.data,
        date_posted = shipment_form.date_posted.data,
        date_received= shipment_form.date_posted.data,
        next_due = shipment_form.next_due.data
          #need to change and create the form 
        )
        db.session.add(pack_added)
        db.session.commit()
        return redirect(url_for('ui.shipment_home'))

     return render_template('ui/pack_shipments/add_shipments.html',shipment_form=shipment_form)

@blueprint.route('/delete_shipments/<int:id>', methods=['GET', 'POST'])
def delete_shipments(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PackShipments).where(PackShipments.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.shipment_home'))
    return render_template('ui/pack_shipments/pack_shipments_home.html', id=id)


@blueprint.route('/edit_shipments/<int:id>', methods=['GET', 'POST'])
def edit_shipments(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PackShipments).where(PackShipments.id == edit_id)).scalar()
        prev_pack_identity = query_edit.pack_identity 
        prev_pack_expiry = query_edit.pack_expiry
        prev_addresse= query_edit.addressee
        prev_date_posted =query_edit.date_posted 
        prev_date_received =query_edit.date_recieved
        prev_next_due= query_edit.next_due

        ed_form=ShipmentForm(pack_identity=prev_pack_identity, pack_expiry=prev_pack_expiry, addressee=prev_addresse,date_posted=prev_date_posted
                             ,date_received=prev_date_received, next_due=prev_next_due) 

    
    if ed_form.validate_on_submit():
            query_edit.pack_identity = ed_form.pack_identity .data
            query_edit.pack_expiry= ed_form.pack_expiry
            query_edit.addressee = ed_form.addressee
            query_edit.date_posted = ed_form.date_posted
            query_edit.date_received = ed_form.date_received
            query_edit.next_due = ed_form.next_due
            db.session.add(query_edit)
            db.session.commit()
            return redirect(url_for('ui.shipment_home'))
        

    return render_template('ui/pack_shipments/edit_shipments.html', ed_form = ed_form, id=id)
