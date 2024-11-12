from flask import render_template, redirect,url_for
from .. import blueprint
from coloprevent.model import Site
from lbrc_flask.database import db


@blueprint.route('/summary', methods=['GET', 'POST'])
def summary():
    q_list = db.session.execute(db.select(Site).order_by(Site.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)
    return render_template('ui/summary.html', order_list = ordered_list)
    