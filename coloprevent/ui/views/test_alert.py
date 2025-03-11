from .. import blueprint
from flask import render_template
#from coloprevent.model import  Pack, Site, PackShipment

@blueprint.route("/is_updating")
def is_updating():
    count=5
    return render_template("ui/alerts/updating.html", count=count)


