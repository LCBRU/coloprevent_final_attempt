from .. import blueprint
from flask import render_template
from lbrc_flask.database import db
from coloprevent.model import  Pack
from sqlalchemy import select, desc
from datetime import *


today = date.today()
print(today)

expiry_alert_list= []



print(f" today is {today}")

@blueprint.route("/is_updating")
def is_updating():
    expiry_alert = False
    q = db.select(Pack.pack_expiry).order_by(Pack.pack_expiry)
    q_date = db.session.execute(q).scalars()
    for dat_dif in q_date:
        calc_diff= (today - dat_dif).days
        print(calc_diff)
        print(type(calc_diff))
        if calc_diff >= 30:
            expiry_alert_list.append(calc_diff)
    if len(expiry_alert_list) >= 1:
        expiry_alert = True
          
    
    return render_template("ui/alerts/updating.html", expiry_alert=expiry_alert)


