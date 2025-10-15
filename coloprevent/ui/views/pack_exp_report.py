from .. import blueprint
from flask import render_template, request, send_file
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from wtforms import DateField, SelectField
from lbrc_flask.forms import SearchForm
from coloprevent.model import  Pack, Site, PackShipment, PackType
import csv


class DropDownForm (SearchForm):
    packtype = SelectField('Packtype')
    pack_expriry_from = DateField()
    pack_expriry_to = DateField()
    pack_specific_expiry_date = DateField()
    site = SelectField ('Site')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.packtype.choices=[("","")]+[(pk.id, pk.packtype_name) for pk in db.session.execute(select(PackType)).scalars()]
        self.site.choices=[("","")]+[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]


@blueprint.route('/pack_expiry_report')
def pack_expiry_report():
   search_form = DropDownForm(search_placeholder='Search Pack ID', formdata=request.args)
   q = get_pack_expiry_report_query(search_form)
   
   results = db.session.execute(q).mappings()
   return render_template( "ui/reports/pack_exp_report.html", results=results, search_form=search_form)


@blueprint.route('/pack_expiry_report_download')
def pack_expiry_report_download():
   search_form = DropDownForm(formdata=request.args)
   q = get_pack_expiry_report_query(search_form)
   
   packs = db.session.execute(q).all()

   with open ('expiry_csv', 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile , delimiter=',')
      csvwriter.writerow(["Pack Identity", "Packtype", "Pack Expiry", "Site"])
      for q_line in packs:
         csvwriter.writerow([q_line.pack_identity, q_line.packtype_name, q_line.pack_expiry, q_line.site_name])

   return send_file('../expiry_csv',
      mimetype='text/csv',
      as_attachment=True,
      download_name="Expiry_report.csv"
   )


def get_pack_expiry_report_query(search_form):
    q = db.select(        #added db.
      Pack.pack_identity,
      Pack.pack_expiry,
      PackType.packtype_name,
      Site.site_name,
   ).join(Pack.packtype
   ).join(
      Pack.pack_shipment
   ).join(
      PackShipment.site)

    if search_form.search.data:
       q = q.where(Pack.pack_identity == search_form.search.data)

    if search_form.packtype.data:
       q = q.where(PackType.id == search_form.packtype.data)
   
    if search_form.pack_expriry_from.data:
       q = q.where(Pack.pack_expiry > search_form.pack_expriry_from.data)

    if search_form.pack_expriry_to.data:
       q = q.where(Pack.pack_expiry < search_form.pack_expriry_to.data)

    if search_form.pack_specific_expiry_date.data:
       q = q.where(Pack.pack_expiry == search_form.pack_specific_expiry_date.data)

    if search_form.site.data:
       q = q.where(PackShipment.site_id == search_form.site.data)
    return q
  


