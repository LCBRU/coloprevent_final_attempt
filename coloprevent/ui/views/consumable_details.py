from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField, FloatField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import ConsumableDetails, Consumable
from flask_wtf import FlaskForm

@blueprint.route('/consumable_details_home', methods=['GET', 'POST'])
def consumable_details_home():
    search_form = SearchForm(search_placeholder='Search consumable details', formdata=request.args) 

    q_list = db.session.execute(db.select(ConsumableDetails).order_by(ConsumableDetails.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(ConsumableDetails.cat_no.like(f'%{search_form.search.data}%'))
    return render_template('ui/consumable_details/consumable_details_home.html', ordered_list = ordered_list, search_form=search_form)

class ConsumableDetailsForm(FlaskForm):
    cat_no = StringField('Cat no', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    price_increase = IntegerField('Price increase', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity_per_pack = IntegerField('Quantity per pack', validators=[DataRequired()])
    consumable = IntegerField('Consumable')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.consumable.choices=[(c.id, c.consumable_name) for c in db.session.execute(select(Consumable)).scalars()]


@blueprint.route('/add_consumable_details', methods=['GET', 'POST'])
def add_consumable_details ():
    consumable_details_form = ConsumableDetailsForm()
    if consumable_details_form.validate_on_submit():
        consumable_details_added = ConsumableDetails(
        cat_no = consumable_details_form.cat_no.data,
        supplier = consumable_details_form.supplier.data,
        price_increase = consumable_details_form.price_increase.data,
        price = consumable_details_form.price.data,
        quantity_per_pack = consumable_details_form.quantity_per_pack.data,
        cons_name_id = consumable_details_form.consumable.data
        )
        db.session.add(consumable_details_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=consumable_details_form, title="Add Consumable details", url=url_for("ui.add_consumable_details"))
    

@blueprint.route('/delete_consumable_details/<int:id>', methods=['GET', 'POST'])
def delete_consumable_details(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(ConsumableDetails).where(ConsumableDetails.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.consumable_details_home'))
    return render_template('ui/consumable_details/delete_consumable_details.html', id=id)


@blueprint.route('/edit_consumable_details/<int:id>', methods=['GET', 'POST'])
def edit_consumable_details(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(ConsumableDetails).where(ConsumableDetails.id == edit_id)).scalar()
        prev_cat_no = query_edit.cat_no
        prev_supplier = query_edit.supplier
        prev_price_increase = query_edit.price_increase
        prev_price = query_edit.price
        prev_quantity_per_pack = query_edit.quantity_per_pack
        prev_consumable= query_edit.cons_name_id


        ed_form=ConsumableDetailsForm(cat_no=prev_cat_no, supplier=prev_supplier, price_increase=prev_price_increase, price=prev_price,
                                       quantity_per_pack=prev_quantity_per_pack, consumable=prev_consumable) 

    
    if ed_form.validate_on_submit():
            query_edit.cat_no = ed_form.cat_no.data
            query_edit.supplier = ed_form.supplier.data
            query_edit.price_increase = ed_form.price_increase.data
            query_edit.price = ed_form.price.data
            query_edit.quantity_per_pack = ed_form.quantity_per_pack.data
            query_edit.cons_name_id = ed_form.consumable.data 
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Consumable details", url=url_for("ui.edit_consumable_details",id=id))
















