from .. import blueprint
from flask import render_template, request, send_file
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from wtforms import DateField, SelectField
from lbrc_flask.forms import SearchForm
from coloprevent.model import  Pack, Site, PackShipment, PackType
import csv
from tempfile import NamedTemporaryFile
import datetime


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
   
   packs = db.session.execute(q).mappings().all()

   headers = {
   'Pack Identity': None,
   'Packtype': None,
   'Pack Expiry': None,
   'Site': None,
}

   expiry_details = ({
   'Pack Identity':pack.pack_identity,
   'Packtype': pack.packtype_name,
   'Pack Expiry': pack.pack_expiry,
   'Site': pack.site_name,
   } for pack in packs)

   return csv_download('Expiries', headers.keys(), expiry_details)

def csv_download(title: str, headers: list[str], details: list[dict]):
    with NamedTemporaryFile(mode='w+', delete=True, encoding='utf-8') as tmp:
        writer = csv.DictWriter(tmp, fieldnames=list(headers))

        writer.writeheader()

        for d in details:
            writer.writerow(d)

        tmp.flush()
        tmp.seek(0)

        return send_file(
            tmp.name,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{title}_{datetime.datetime.now(datetime.UTC):%Y%m%d_%H%M%S}.csv',
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
  


