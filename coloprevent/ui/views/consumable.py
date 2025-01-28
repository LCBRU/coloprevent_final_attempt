from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Consumable
from flask_wtf import FlaskForm

@blueprint.route('/consumable', methods=['GET', 'POST'])
def consumable_home():
    search_form = SearchForm(search_placeholder='Search consumable name', formdata=request.args) 

    q_list = db.session.execute(db.select(Consumable).order_by(Consumable.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(Consumable.consumable_name.like(f'%{search_form.search.data}%'))
    return render_template('ui/consumables/consumable_home.html', ordered_list = ordered_list, search_form=search_form)

class ConsumableForm(FlaskForm):
    consumable_name = StringField('Consumable', validators=[DataRequired()])

@blueprint.route('/add_consumable', methods=['GET', 'POST'])
def add_consumable ():
    consumable_form = ConsumableForm()
    if consumable_form.validate_on_submit():
        consumable_added = Consumable(
        consumable_name= consumable_form.consumable_name.data,
        )
        db.session.add(consumable_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=consumable_form, title="Add Consumable", url=url_for("ui.add_consumable"))



@blueprint.route('/delete_consumable/<int:id>', methods=['GET', 'POST'])
def delete_consumable(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Consumable).where(Consumable.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.consumable_home'))
    return render_template('ui/consumables/delete_consumable.html', id=id)



@blueprint.route('/edit_consumable/<int:id>', methods=['GET', 'POST'])
def edit_consumable(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Consumable).where(Consumable.id == edit_id)).scalar()
        prev_consumable_name = query_edit.consumable_name

        ed_form=ConsumableForm(consumable_name=prev_consumable_name) 

    
    if ed_form.validate_on_submit():
            query_edit.consumable_name= ed_form.consumable_name.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Consumable", url=url_for("ui.edit_consumable",id=id))