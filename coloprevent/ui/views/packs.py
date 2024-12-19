from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, DateField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm
from lbrc_flask.response import refresh_response
from coloprevent.model import Packs
from flask_wtf import FlaskForm

@blueprint.route('/packs', methods=['GET', 'POST'])
def packs():
    q_list = db.session.execute(db.select(Packs).order_by(Packs.id)).scalars()  #need to re configure this table 
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)
    return render_template('ui/packs/packs_home.html', order_list = ordered_list)

class PackForm(FlaskForm):
    pack_id = StringField('Pack name', validators=[DataRequired()])
    pack_expiry = DateField(format='%Y-%m-%d')



@blueprint.route('/add_pack', methods=['GET', 'POST'])
def add_pack():
    pack_form = PackForm()
    if pack_form.validate_on_submit():
        pack_added = Packs(
        pack_id= pack_form.pack_id.data,
        pack_expiry = pack_form.pack_expiry.data,
        )
        db.session.add(pack_added)
        db.session.commit()
        return redirect(url_for('ui.packs'))
    
    return render_template('ui/packs/add_pack.html', pack_form=pack_form)

@blueprint.route('/delete_pack/<int:id>', methods=['GET', 'POST'])
def delete_pack(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Packs).where(Packs.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.packs'))
    return render_template('ui/packs/delete_pack.html', id=id)

@blueprint.route('/edit_pack/<int:id>', methods=['GET', 'POST'])
def edit_pack(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Packs).where(Packs.id == edit_id)).scalar()
        prev_pack_name = query_edit.name
        ed_form=PackForm(pack_name=prev_pack_name) 

    
    if ed_form.validate_on_submit():
            query_edit.name= ed_form.pack_name.data
            db.session.add(query_edit)
            db.session.commit()
            return redirect(url_for('ui.packs'))
        

    return render_template('ui/packs/edit_pack.html', ed_form = ed_form, id=id)