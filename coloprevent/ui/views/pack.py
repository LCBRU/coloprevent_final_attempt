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
from coloprevent.model import PackType, Pack
from flask_wtf import FlaskForm

@blueprint.route('/pack', methods=['GET', 'POST'])
def pack():
    search_form = SearchForm(search_placeholder='Search packs ID', formdata=request.args) 
    q = db.select(Pack).order_by(Pack.pack_expiry, Pack.id)
    if search_form.search.data:
        q = q.where(Pack.pack_identity.like(f'%{search_form.search.data}%'))

    packs = db.paginate(
    select=q,
    page=search_form.page.data,
    per_page=5,
    error_out=False,
)


    # q_list = db.session.execute(q).scalars()
    # ordered_list =[]
    # for queried in q_list:
    #     ordered_list.append(queried)

    return render_template('ui/pack/pack_home.html',packs=packs, search_form=search_form)

class PackForm(FlashingForm):
    pack_identity = StringField('Pack Identity', validators=[DataRequired()])
    pack_expiry = DateField(format='%Y-%m-%d')
    pack_type = RadioField('Packtype' , coerce=int)

    def __init__(self, **kwargs):
        super().__init__( **kwargs)

        self.pack_type.choices=[(p.id, p.packtype_name) for p in db.session.execute(select(PackType)).scalars()]



@blueprint.route('/add_pack', methods=['GET', 'POST'])
def add_pack():
    pack_form = PackForm()
    if pack_form.validate_on_submit():
        pack_id_data = pack_form.pack_identity.data.split("-") 
        for packid in pack_id_data:
            
            pack_added = Pack(
            pack_identity= int(packid),
            pack_expiry = pack_form.pack_expiry.data,
            packtype_id = pack_form.pack_type.data
            )
            db.session.add(pack_added)
            db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=pack_form , title="Add Pack", url=url_for("ui.add_pack"))

class PackActionForm(FlashingForm):
    pack_action = RadioField(u'Tick "Yes" to ignore the expiry alert from this pack', choices=[('Yes', 'Yes'), ('No', 'No')])

@blueprint.route('/pack_action/<int:id>', methods=['GET', 'POST'])
def pack_action(id):
    find_record = db.get_or_404(Pack,id)
    add_pack_action_form = PackActionForm()
    if add_pack_action_form.validate_on_submit():
        find_record.pack_action = add_pack_action_form.pack_action.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_pack_action_form, id=id, title="Click yes to ignore from report", url=url_for("ui.pack_action",id=id))
    


@blueprint.route('/delete_pack/<int:id>', methods=['GET', 'POST'])
def delete_pack(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Pack).where(Pack.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.pack'))
    return render_template('ui/pack/delete_pack.html', id=id)

@blueprint.route('/edit_pack/<int:id>', methods=['GET', 'POST'])
def edit_pack(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Pack).where(Pack.id == edit_id)).scalar()
        prev_pack_identity = query_edit.pack_identity
        prev_pack_expiry = query_edit.pack_expiry
        prev_packtype_form = query_edit.packtype_id
        
        ed_form=PackForm(pack_identity=prev_pack_identity, pack_expiry=prev_pack_expiry, pack_type=prev_packtype_form) 

    
    if ed_form.validate_on_submit():
            query_edit.pack_identity= ed_form.pack_identity.data
            query_edit.pack_expiry= ed_form.pack_expiry.data
            query_edit.packtype_id = ed_form.pack_type.data 
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html',form = ed_form, id=id, title="Edit Pack", url=url_for("ui.edit_pack",id=id))