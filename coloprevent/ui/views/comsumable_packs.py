from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import ConsumableDetails, Consumable,ConsumablePacks
from flask_wtf import FlaskForm

@blueprint.route('/consumable_packs_home', methods=['GET', 'POST'])
def consumable_packs_home():
    search_form = SearchForm(search_placeholder='Search consumable packs', formdata=request.args) 

    q_list = db.session.execute(db.select(ConsumablePacks).order_by(ConsumablePacks.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(ConsumablePacks.date_received.like(f'%{search_form.search.data}%'))
    return render_template('ui/consumable_packs/consumable_packs_home.html', ordered_list = ordered_list, search_form=search_form)


class ConsumablePacksForm(FlaskForm):
    date_received = DateField('Date recieved', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    number_of_packs = IntegerField('Number of packs', validators=[DataRequired()])
    consumable = IntegerField('Consumable Name')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.consumable.choices=[(c.id, c.consumable_name) for c in db.session.execute(select(Consumable)).scalars()]


@blueprint.route('/add_consumable_packs', methods=['GET', 'POST'])
def add_consumable_packs ():
    consumable_packs_form = ConsumablePacksForm()
    if consumable_packs_form.validate_on_submit():
        consumable_packs_added = ConsumablePacks(
            date_received = consumable_packs_form.date_receieved.data,
            cost = consumable_packs_form.cost.data,
            number_of_packs = consumable_packs_form.number_of_packs.data,
            cons_name_id = consumable_packs_form.consumable.data,
             
        )
        db.session.add(consumable_packs_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=consumable_packs_form, title="Add Packs estimates", url=url_for("ui.add_consumable_packs"))

@blueprint.route('/delete_consumable_packs/<int:id>', methods=['GET', 'POST'])
def delete_consumable_packs(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(ConsumablePacks).where(ConsumablePacks.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.consumable_packs_home'))
    return render_template('ui/consumable_packs/delete_consumable_packs.html', id=id)

@blueprint.route('/edit_consumable_packs/<int:id>', methods=['GET', 'POST'])
def edit_consumable_packs(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(ConsumablePacks).where(ConsumablePacks.id == edit_id)).scalar()
        prev_date_received = query_edit.date_received 
        prev_cost = query_edit.cost
        prev_number_of_packs = query_edit.number_of_packs
        prev_consumable = query_edit.cons_name_id
      


        ed_form=ConsumablePacksForm(date_received=prev_date_received, cost=prev_cost, number_of_packs=prev_number_of_packs,
                                       consumable=prev_consumable) 

    
    if ed_form.validate_on_submit():
            query_edit.date_received = ed_form.date_received.data
            query_edit.cost = ed_form.cost.data
            query_edit.number_of_packs = ed_form.number_of_packs.data 
            query_edit.cons_name_id = ed_form.consumable.data 
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Consumable packs", url=url_for("ui.edit_consumable_packs",id=id))