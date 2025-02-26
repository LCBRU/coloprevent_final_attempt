from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import  Pack, Site, PackShipment
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments


@blueprint.route('/pack_expiry_report', methods=['GET', 'POST'])
def pack_expiry_report():
   q = select(
   Pack.pack_identity,
   Pack.pack_expiry,
   # Pack.pack_shipment_id,
   Site.site_name,
   ).join(
   Pack.pack_shipment
   ).join(
   PackShipment.site,
   )



   # Site.site_name,).join
   # (Pack.id).join
   # (PackShipment.id)
   # Pack.pack_identity,
   #  Pack.pack_expiry,
   #  Site.site_name
   # ).join(
   #  Site, PackShipment.site_id == Site.id
   # ).join(
   #  Pack, PackShipment.packs == Pack.id
   # )
   


   results = db.session.execute(q).mappings()
   return render_template( "ui/reports/pack_exp_report.html", results=results)
  


