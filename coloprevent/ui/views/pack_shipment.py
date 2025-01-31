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
from coloprevent.model import PackShipment, Pack, Site
from flask_wtf import FlaskForm


@blueprint.route('/shipment', methods=['GET', 'POST'])
def shipment_home():
     search_form = SearchForm(search_placeholder='Search shipment via packs identifier', formdata=request.args) 

     q_list = db.session.execute(db.select(PackShipment).order_by(PackShipment.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)

     if search_form.search.data:
        q = q.where(PackShipment.site.like(f'%{search_form.search.data}%'))
 
     return render_template('ui/pack_shipment/pack_shipment_home.html/', ordered_list=ordered_list, search_form=search_form)



class ShipmentForm(FlaskForm):
    addressee =TextAreaField(label="Addressee", validators=[DataRequired()])
    date_posted = DateField(format='%Y-%m-%d')
    date_received = DateField(format='%Y-%m-%d')
    next_due = DateField(format='%Y-%m-%d')
    pack = IntegerField('Packs ID')  #new change
    site = IntegerField('Site') #new change

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.pack.choices=[(p.id, p.pack_identity) for p in db.session.execute(select(Pack)).scalars()]
        self.site.choices=[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]
    
   

@blueprint.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
     shipment_form = ShipmentForm()
     if shipment_form.validate_on_submit():
        pack_added = PackShipment(
            addressee= shipment_form.addressee.data,
            date_posted = shipment_form.date_posted.data,
            date_received= shipment_form.date_received.data,
            next_due = shipment_form.next_due.data,
            pack_id = shipment_form.pack.data,
            site_id = shipment_form.site.data
          
        )
        db.session.add(pack_added)
        db.session.commit()
        return refresh_response()

     return render_template('lbrc/form_modal.html', form=shipment_form, title="Add Shipment", url=url_for("ui.add_shipment") )

@blueprint.route('/delete_shipment/<int:id>', methods=['GET', 'POST'])
def delete_shipment(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PackShipment).where(PackShipment.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.shipment_home'))
    return render_template('ui/pack_shipment/pack_shipment_home.html', id=id)


@blueprint.route('/edit_shipment/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PackShipment).where(PackShipment.id == edit_id)).scalar()
        prev_addresse= query_edit.addressee
        prev_date_posted =query_edit.date_posted 
        prev_date_received =query_edit.date_received 
        prev_next_due= query_edit.next_due
        prev_pack = query_edit.pack_id
        prev_site = query_edit.site_id

        ed_form=ShipmentForm(addressee=prev_addresse,date_posted=prev_date_posted
                             ,date_received=prev_date_received, next_due=prev_next_due, pack=prev_pack, site=prev_site)

    
    if ed_form.validate_on_submit():
            query_edit.addressee = ed_form.addressee.data
            query_edit.date_posted = ed_form.date_posted.data
            query_edit.date_received = ed_form.date_received.data
            query_edit.next_due = ed_form.next_due.data
            query_edit.pack_id = ed_form.pack.data
            query_edit.site_id = ed_form.site.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Shipment", url=url_for("ui.edit_shipments",id=id))
