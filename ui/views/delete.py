from .. import blueprint
from flask import render_template, redirect,url_for
from coloprevent.model import Site
from lbrc_flask.database import db

@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Site).where(Site.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect("/summary")
    return render_template('delete.html', id=id)