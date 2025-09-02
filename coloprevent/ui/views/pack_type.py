from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from wtforms import StringField
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PackType
from wtforms.validators import DataRequired, Length


class PacktypeForm(FlashingForm):
    packtype_name = StringField("Name", validators=[DataRequired(), Length(max=100)])

@blueprint.route('/packtype_home', methods=['GET', 'POST'])
def packtype_home():
    search_form = SearchForm(search_placeholder='Search packtype Name', formdata=request.args)
    q = db.select(PackType).order_by(PackType.id)
    if search_form.search.data:
        q = q.where(PackType.packtype_name.like(f'%{search_form.search.data}%'))


    packtypes = db.paginate(
    select=q,
    page=search_form.page.data,
    per_page=5,
    error_out=False,
)

    return render_template('ui/packtype/packtype_home.html', packtypes=packtypes, search_form=search_form)

@blueprint.route('/add_packtype', methods=['GET', 'POST'])
def add_packtype():
     packtypes_form = PacktypeForm()
     if packtypes_form.validate_on_submit():
        pack_added = PackType(
        packtype_name= packtypes_form.packtype_name.data
        )
        db.session.add(pack_added)
        db.session.commit()
        return refresh_response()

     return render_template('lbrc/form_modal.html',form=packtypes_form,title="Add Packtype", url=url_for("ui.add_packtype")) 


@blueprint.route('/delete_packtype/<int:id>', methods=['GET', 'POST'])
def delete_packtype(id):
    item = db.session.get(PackType, id)

    if item is not None:
        db.session.delete(item)
        db.session.commit()

    return refresh_response()


@blueprint.route('/edit_packtype/<int:id>', methods=['GET', 'POST'])
def edit_packtype(id):
    edit_id = id
    if id== edit_id:
        query_edit =db.session.execute(db.select(PackType).where(PackType.id == edit_id)).scalar()
        prev_packtype_name = query_edit.packtype_name
        ed_form=PacktypeForm(pack_type_name=prev_packtype_name) 

    
    if ed_form.validate_on_submit():
            query_edit.packtype_name= ed_form.packtype_name.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Packtype", url=url_for("ui.edit_packtype" ,id=id))

