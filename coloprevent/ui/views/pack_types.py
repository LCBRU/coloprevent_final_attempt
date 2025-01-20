from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, RadioField, widgets, SubmitField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PackTypes
from flask_wtf import FlaskForm

class PacktypeForm(FlaskForm):
    packtype_name = RadioField('Packtypes',choices=[('Screening', 'Screening'), ('Fit', 'FIT'), ('Research', 'Research'), ('Tissue_ffpe', 'Tissue/FFPE')])

@blueprint.route('/packtypes_home', methods=['GET', 'POST'])
def packtypes_home():
    search_form = SearchForm(search_placeholder='Search packtype Name', formdata=request.args) 

    q_list = list(db.session.execute(db.select(PackTypes).order_by(PackTypes.id)).scalars())

    if search_form.search.data:
        q = q.where(PackTypes.pack_identity.like(f'%{search_form.search.data}%'))

    return render_template('ui/packtypes/packtypes_home.html', ordered_list=q_list, search_form=search_form)

@blueprint.route('/add_packtypes', methods=['GET', 'POST'])
def add_packtypes():
     packtypes_form = PacktypeForm()
     if packtypes_form.validate_on_submit():
        pack_added = PackTypes(
        packtype_name= packtypes_form.packtype_name.data
        )
        db.session.add(pack_added)
        db.session.commit()
        return refresh_response()

     return render_template('lbrc/form_modal.html',form=packtypes_form,title="Add Packtype", url=url_for("ui.add_packtypes")) 


@blueprint.route('/delete_packtypes/<int:id>', methods=['GET', 'POST'])
def delete_packtypes(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PackTypes).where(PackTypes.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.packtypes_home'))
    return render_template('ui/packtypes/delete_packtypes.html', id=id)


@blueprint.route('/edit_packtypes/<int:id>', methods=['GET', 'POST'])
def edit_packtypes(id):
    edit_id = id
    if id== edit_id:
        query_edit =db.session.execute(db.select(PackTypes).where(PackTypes.id == edit_id)).scalar()
        prev_packtype_name = query_edit.packtype_name
        ed_form=PacktypeForm(pack_type_name=prev_packtype_name) 

    
    if ed_form.validate_on_submit():
            query_edit.packtype_name= ed_form.packtype_name.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', ed_form = ed_form, id=id, title="Edit Packtype", url=url_for("ui.edit_packtypes, id=id"))

