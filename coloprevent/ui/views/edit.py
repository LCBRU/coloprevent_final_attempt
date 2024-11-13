from .. import blueprint
from flask import render_template, redirect,url_for
from coloprevent.model import Site
from lbrc_flask.database import db
from add import SiteForm

@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Site).where(Site.id == edit_id)).scalar()
        prev_site_name = query_edit.site_name
        ed_form=SiteForm(site_name=prev_site_name) 

    
    if ed_form.validate_on_submit():
            query_edit.site_name= ed_form.site_name.data
            db.session.add(query_edit)
            db.session.commit()
            return redirect("/summary")
        

    return render_template('edit.html', ed_form = ed_form, id=id)