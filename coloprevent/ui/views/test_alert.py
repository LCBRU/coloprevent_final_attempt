from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
#from coloprevent.model import  Pack, Site, PackShipment
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments

@blueprint.route("/is_updating")
def is_updating():
    count=5
    return render_template("ui/alerts/updating.html", count=count)


