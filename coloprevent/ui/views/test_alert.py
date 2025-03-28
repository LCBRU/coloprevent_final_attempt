from .. import blueprint
from flask import render_template
from lbrc_flask.database import db
from coloprevent.model import  Pack
from sqlalchemy import select, func
from datetime import *


@blueprint.route("/is_updating")
def is_updating():
    expiry_date = date.today()-timedelta(days=30)
    q = db.select(func.count(Pack.id)).where(Pack.pack_expiry <=expiry_date)
    expiry_alert = db.session.execute(q).scalar() >0

    return render_template("ui/alerts/updating.html", expiry_alert=expiry_alert)


