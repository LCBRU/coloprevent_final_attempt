from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, DateField, IntegerField, RadioField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PackTypes, Packs
from flask_wtf import FlaskForm

@blueprint.route('/packs', methods=['GET', 'POST'])
def packs():
    search_form = SearchForm(search_placeholder='Search packs ID', formdata=request.args) 

    q_list = db.session.execute(db.select(Packs).order_by(Packs.id)).scalars()  
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(Packs.identifier.like(f'%{search_form.search.data}%'))

    return render_template('ui/packs/packs_home.html', ordered_list = ordered_list, search_form=search_form)

class PackForm(FlaskForm):
    pack_identity = StringField('Pack ID', validators=[DataRequired()])
    pack_quantity = IntegerField('Quantity', validators=[DataRequired()])
    pack_expiry = DateField(format='%Y-%m-%d', validators=[DataRequired()])
    pack_type = RadioField('Packtypes' , coerce=int)

    def __init__(self, **kwargs):
        super().__init__( **kwargs)

        self.pack_type.choices=[(p.id, p.packtype_name) for p in db.session.execute(select(PackTypes)).scalars()]



@blueprint.route('/add_pack', methods=['GET', 'POST'])
def add_pack():
    pack_form = PackForm()
    if pack_form.validate_on_submit():
        pack_added = Packs(
        pack_identity= pack_form.pack_identity.data,
        pack_quantity = pack_form.pack_quantity.data,
        pack_expiry = pack_form.pack_expiry.data,
        packtypes_id = pack_form.pack_type.data
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
        prev_pack_identity = query_edit.pack_identity,
        prev_pack_quantity = query_edit.pack_quantity,
        prev_pack_expiry = query_edit.pack_expiry,
        prev_packtype_form = query_edit.packtypes_id
        
        ed_form=PackForm(pack_identity=prev_pack_identity, pack_quantity=prev_pack_quantity, pack_name=prev_pack_expiry, pack_type=prev_packtype_form) 

    
    if ed_form.validate_on_submit():
            query_edit.pack_expiry= ed_form.pack_expiry.data
            query_edit.pack_quantity = ed_form.pack_quantity.data 
            query_edit.pack_identity= ed_form.pack_identity.data
            query_edit.packtypes_id = ed_form.pack_type.data 
            db.session.add(query_edit)
            db.session.commit()
            return redirect(url_for('ui.packs'))
        

    return render_template('ui/packs/edit_pack.html', ed_form = ed_form, id=id)