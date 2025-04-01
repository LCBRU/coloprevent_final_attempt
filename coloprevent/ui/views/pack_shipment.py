from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select, or_
from wtforms import RadioField, DateField, SelectField
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response, refresh_results
from coloprevent.model import PackShipment, Pack, Site, PackType
from lbrc_flask.requests import get_value_from_all_arguments

class SiteDropDownForm (SearchForm):
    site = SelectField('Site ID')
    date_posted_from = DateField()
    date_posted_to = DateField()
    pack_type_id = SelectField('Packtype')
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.site.choices=[("","")]+[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]

        self.pack_type_id.choices=[("","")]+[(pt.id, pt.packtype_name) for pt in db.session.execute(select(PackType)).scalars()]


@blueprint.route('/', methods=['GET', 'POST'])
def index():
     search_form = SiteDropDownForm(search_placeholder='Search by site', formdata=request.args) 
     q = db.select(PackShipment).order_by(PackShipment.id)
     if search_form.search.data:
       q = q.where(

            PackShipment.site.has(Site.site_name.like(f"%{search_form.search.data}%")),
    
    
    )
       
     if search_form.site.data:
        q = q.where(
       
        PackShipment.site_id == search_form.site.data)

     if search_form.date_posted_from.data:
          q = q.where(
       
        PackShipment.date_posted > search_form.date_posted_from.data)
  
     if search_form.date_posted_to.data:
          q = q.where(
       
        PackShipment.date_posted < search_form.date_posted_to.data)
          
     
     if search_form.pack_type_id.data:
         q= q.where (PackShipment.packs.any(Pack.packtype_id == search_form.pack_type_id.data))

    

    

     
     q_list = db.session.execute(q).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)
 
     return render_template('ui/pack_shipment/pack_shipment_home.html', ordered_list=ordered_list, search_form=search_form)



class ShipmentForm(FlashingForm):
    date_posted = DateField(format='%Y-%m-%d')
    site = RadioField('Site') 

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.site.choices=[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]

class ShipmentDate1Form(FlashingForm):
    date_received = DateField(format='%Y-%m-%d')

class ShipmentDate2Form(FlashingForm):
    next_due = DateField(format='%Y-%m-%d')

class EditShipmentForm(FlashingForm):
    date_posted = DateField(format='%Y-%m-%d')
    date_received = DateField(format='%Y-%m-%d')
    next_due = DateField(format='%Y-%m-%d')
    site = RadioField('Site') 

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.site.choices=[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]

    
   

@blueprint.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
     shipment_form = ShipmentForm()
     if shipment_form.validate_on_submit():
        pack_added = PackShipment(
            date_posted = shipment_form.date_posted.data,
            site_id = shipment_form.site.data
          
        )
        db.session.add(pack_added)
        db.session.commit()
        return refresh_response()

     return render_template('lbrc/form_modal.html', form=shipment_form, title="Add Shipment", url=url_for("ui.add_shipment") )

@blueprint.route('/add_shipment_received/<int:id>', methods=['GET', 'POST'])
def add_shipment_received(id):
    find_record = db.get_or_404(PackShipment,id)
    prev_date_received = find_record.date_received
    add_date_form = ShipmentDate1Form(date_received = prev_date_received)
    if add_date_form.validate_on_submit():
        find_record.date_received = add_date_form.date_received.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_date_form, id=id, title="Add received date", url=url_for("ui.add_shipment_received",id=id))

@blueprint.route('/add_shipment_next_due/<int:id>', methods=['GET', 'POST'])
def add_shipment_next_due(id):
    find_record = db.get_or_404(PackShipment, id)
    prev_next_due = find_record.next_due
    add_date_form = ShipmentDate2Form(next_due = prev_next_due)
    if add_date_form.validate_on_submit():
        find_record.next_due = add_date_form.next_due.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_date_form, id=id, title="Add next due date", url=url_for("ui.add_shipment_next_due",id=id))
   



@blueprint.route('/delete_shipment/<int:id>', methods=['GET', 'POST'])
def delete_shipment(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PackShipment).where(PackShipment.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.index'))
    return render_template('ui/pack_shipment/pack_shipment_home.html', id=id)


@blueprint.route('/edit_shipment/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PackShipment).where(PackShipment.id == edit_id)).scalar()
        prev_date_posted =query_edit.date_posted 
        prev_date_received =query_edit.date_received 
        prev_next_due= query_edit.next_due
        prev_site = query_edit.site_id

        ed_form=EditShipmentForm(date_posted=prev_date_posted
                             ,date_received=prev_date_received, next_due=prev_next_due, site=prev_site)

    
    if ed_form.validate_on_submit():
            query_edit.date_posted = ed_form.date_posted.data
            query_edit.date_received = ed_form.date_received.data
            query_edit.next_due = ed_form.next_due.data
            query_edit.site_id = ed_form.site.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html', form = ed_form, id=id, title="Edit Shipment", url=url_for("ui.edit_shipment",id=id))




@blueprint.route("/add_shipment/add_pack/<int:id>/")
def search_pack(id):
    p: PackShipment = db.get_or_404(PackShipment, id)
    return render_template(
    "lbrc/search.html",
    title=f"Add packs to shipment for site '{p.site.site_name}'",
    results_url=url_for('ui.search_pack_search_results', id=p.id),
 
)

class SelectedPack():
    def __init__(self, pack, selected):
        self.name = pack.name
        self.id = pack.id
        self.selected = selected
    

@blueprint.route("/add_shipment/add_pack/<int:id>/search_results/<int:page>")   
@blueprint.route("/add_shipment/add_pack/<int:id>/search_results")
def search_pack_search_results(id, page=1):
    shipment: PackShipment = db.get_or_404(PackShipment, id)
    search = get_value_from_all_arguments('search_string') or ''

    q =  (
        select(Pack)
        .where(or_(
            Pack.pack_shipment_id == None,
            Pack.pack_shipment_id == shipment.id
        ))
        .order_by(Pack.pack_identity, Pack.id)
    )

    if search:
        q = q.where(Pack.pack_identity == search)

    results = db.paginate(select=q)

    new_items = []
    for p in results.items:
        new_items.append(SelectedPack(p, p.pack_shipment_id == shipment.id))

    results.items = new_items

    return render_template(
            "lbrc/search_add_results.html",
            add_title="Add pack shipment" '{q.pack_identity}',
            add_url=url_for('ui.add_pack_to_shipment', id=shipment.id),
            results_url='ui.search_pack_search_results',
            results_url_args={'id': shipment.id},
            results=results,
        )


@blueprint.route("/add_pack/<int:id>/add_pack_to_shipment", methods=['POST'])
def add_pack_to_shipment(id):
    ps = db.get_or_404(PackShipment, id)

    id: int = get_value_from_all_arguments('id')
    pk: Pack = db.get_or_404(Pack, id)

    ps.packs.append(pk) 

    db.session.add(ps)
    db.session.commit()

    return refresh_results()

@blueprint.route("/shipment/<int:id>/pack/<int:pack_id>/delete", methods=['POST'])
def delete_pack_to_shipment(id,pack_id):
    ps = db.get_or_404(PackShipment, id)
    pk: Pack = db.get_or_404(Pack, pack_id)

    ps.packs.remove(pk) 

    db.session.add(ps)
    db.session.commit()

    return refresh_response()