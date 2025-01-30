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
from coloprevent.model import ConsumableDetails, Consumable, ConsumableEstimates
from flask_wtf import FlaskForm


@blueprint.route('/consumable_estimates_home', methods=['GET', 'POST'])
def consumable_estimates_home():
    search_form = SearchForm(search_placeholder='Search consumable estimates by consumable name', formdata=request.args) 

    q_list = db.session.execute(db.select(ConsumableEstimates).order_by(ConsumableEstimates.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(ConsumableEstimates.cons_name_id.like(f'%{search_form.search.data}%'))
    return render_template('ui/consumable_estimates/consumable_estimates_home.html', ordered_list = ordered_list, search_form=search_form)


class ConsumableEstimatesForm(FlaskForm):
    est_number_consumables= IntegerField('Estimated number of consumables', validators=[DataRequired()])
    est_packs_study= IntegerField('Estimated packs for study', validators=[DataRequired()])
    est_cost = FloatField('Estimated costs', validators=[DataRequired()])
    consumable = IntegerField('Consumable Name')
    consumable_details = IntegerField('Cat no')
   

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.consumable.choices=[(c.id, c.consumable_name) for c in db.session.execute(select(Consumable)).scalars()]
        self.consumable_details.choices=[(c_det.id, c_det.cat_no) for c_det in db.session.execute(select(ConsumableDetails)).scalars()]


@blueprint.route('/add_consumable_estimates', methods=['GET', 'POST'])
def add_consumable_estimates ():
    consumable_estimates_form = ConsumableEstimatesForm()
    if consumable_estimates_form.validate_on_submit():
        consumable_estimates_added = ConsumableEstimates(
            est_number_consumables = consumable_estimates_form.est_number_consumables.data,
            est_packs_study = consumable_estimates_form.est_packs_study.data,
            est_cost = consumable_estimates_form.est_cost.data,
            cons_name_id = consumable_estimates_form.consumable.data,
            cons_details_id = consumable_estimates_form.consumable_details.data     
        )
        db.session.add(consumable_estimates_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=consumable_estimates_form, title="Add Consumable estimates", url=url_for("ui.add_consumable_estimates"))

@blueprint.route('/delete_consumable_estimates/<int:id>', methods=['GET', 'POST'])
def delete_consumable_estimates(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(ConsumableEstimates).where(ConsumableEstimates.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.consumable_estimates_home'))
    return render_template('ui/consumable_estimates/delete_consumable_estimates.html', id=id)


@blueprint.route('/edit_consumable_estimates/<int:id>', methods=['GET', 'POST'])
def edit_consumable_estimates(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(ConsumableEstimates).where(ConsumableEstimates.id == edit_id)).scalar()
        prev_est_number_comsumables = query_edit.est_number_consumables 
        prev_est_packs_study = query_edit.est_packs_study
        prev_est_cost = query_edit.est_cost
        prev_consumable = query_edit.cons_name_id
        prev_consumable_details = query_edit.cons_details_id
      


        ed_form=ConsumableEstimatesForm(est_number_consumables=prev_est_number_comsumables,  est_packs_study=prev_est_packs_study, est_cost=prev_est_cost,
                                       consumable=prev_consumable, consumable_details=prev_consumable_details) 

    
    if ed_form.validate_on_submit():
            query_edit.est_number_consumables = ed_form.est_number_consumables.data
            query_edit.est_packs_study = ed_form.est_packs_study.data
            query_edit.est_cost = ed_form.est_cost.data 
            query_edit.cons_name_id = ed_form.consumable.data 
            query_edit.cons_details_id =ed_form.consumable_details.data 
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Consumable estimates", url=url_for("ui.edit_consumable_estimates",id=id))