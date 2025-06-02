from .. import blueprint
from flask import render_template, request, url_for, redirect, send_file
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select, and_
from lbrc_flask.security import User
from wtforms.validators import Length, DataRequired
from wtforms import HiddenField, StringField, TextAreaField, DateField, SelectField, SubmitField
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import  Pack, Site, PackShipment, PackType
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments
import csv


class DropDownForm (SearchForm):
    packtype = SelectField('Packtype')
    pack_expriry_from = DateField()
    pack_expriry_to = DateField()
    site = SelectField ('Site')


    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.packtype.choices=[("","")]+[(pk.id, pk.packtype_name) for pk in db.session.execute(select(PackType)).scalars()]

        self.site.choices=[("","")]+[(s.id, s.site_name) for s in db.session.execute(select(Site)).scalars()]


@blueprint.route('/pack_expiry_report', methods=['GET', 'POST'])
def pack_expiry_report():
   search_form = DropDownForm(search_placeholder='Search Pack ID', formdata=request.args) 
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

   if search_form.site.data:
      q = q.where(PackShipment.site_id == search_form.site.data)

   q_download = db.session.execute(q).scalars()   
   


   if request.method == "POST":
      download_button = request.form.get('download_report')
      if download_button is not None:  
         with open ('expiry_csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile , delimiter=',')
            csvwriter.writerow(["Pack Identity", "Packtype", "Pack Expiry", "Site"])
            for q_line in q_download:
               csvwriter.writerow([q_line.pack_identity, q_line.packtype.packtype_name, q_line.pack_expiry, q_line.packshipment.site_id])

         return send_file('../expiry_csv',
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name="Expiry_report.csv"

                        )

      




   results = db.session.execute(q).mappings()
   return render_template( "ui/reports/pack_exp_report.html", results=results, search_form=search_form)
  


