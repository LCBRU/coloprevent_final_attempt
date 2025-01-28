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
    return render_template('ui/consumables/consumable_details_home.html', ordered_list = ordered_list, search_form=search_form)

class ConsumableDetailsForm(FlaskForm):
    cat_no = StringField('Cat no', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    price_increase = IntegerField('Price increase', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity_per_pack = IntegerField('Quantity per pack', validators=[DataRequired()])
    consumable = IntegerField('Consumable')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.consumable=[(c.id) for c in db.session.execute(select(Consumable)).scalars()]
    

