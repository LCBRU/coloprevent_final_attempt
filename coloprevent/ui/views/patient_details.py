from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PatientDetails
from flask_wtf import FlaskForm

@blueprint.route('/patient_details', methods=['GET', 'POST'])
def patient_details_home():
    search_form = SearchForm(search_placeholder='Search Patient', formdata=request.args) 

    q_list = db.session.execute(db.select(PatientDetails).order_by(PatientDetails.id)).scalars()
    ordered_list =[]
    for queried in q_list:
        ordered_list.append(queried)


    if search_form.search.data:
        q = q.where(PatientDetails.screening_id.like(f'%{search_form.search.data}%'))
    return render_template('ui/patient_details/patient_details_home.html', ordered_list = ordered_list, search_form=search_form)

class PatientDetailsForm(FlaskForm):
    screening_id = StringField('Screening ID', validators=[DataRequired()])
    pid= StringField('PID', validators=[DataRequired()])
    date_of_consent = DateField('Date of consent', validators=[DataRequired()])
    

@blueprint.route('/add_patient_details', methods=['GET', 'POST'])
def add_patient_details ():
    patient_details_form = PatientDetailsForm()
    if patient_details_form.validate_on_submit():
        patient_details_added = PatientDetails(
            screening_id = patient_details_form.screening_id.data,
            pid = patient_details_form.pid,
            date_of_consent = patient_details_form.date_of_consent.data
        )
        db.session.add(patient_details_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=patient_details_form, title="Add patient details", url=url_for("ui.add_patient_details"))


@blueprint.route('/delete_patient_details/<int:id>', methods=['GET', 'POST'])
def delete_patient_details(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PatientDetails).where(PatientDetails.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.patient_details_home'))
    return render_template('ui/patient_details/delete_patient_details.html', id=id)

