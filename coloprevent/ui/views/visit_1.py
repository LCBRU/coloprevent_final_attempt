from .. import blueprint
from flask import render_template, request, url_for, redirect
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User
from wtforms import HiddenField, StringField, RadioField, widgets, SubmitField, DateField, IntegerField,TextAreaField
from wtforms.validators import Length, DataRequired
from lbrc_flask.forms import FlashingForm, SearchForm
from lbrc_flask.response import refresh_response
from coloprevent.model import PatientVisit1, PatientDetails
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments


@blueprint.route('/visit_1', methods=['GET', 'POST'])
def visit_1():
     search_form = SearchForm(search_placeholder='Search screening ID', formdata=request.args) 

     q_list = db.session.execute(db.select(PatientVisit1).order_by(PatientVisit1.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)

     if search_form.search.data:
        q = q.where(PatientDetails.screening_id.like(f'%{search_form.search.data}%'))
 
     return render_template('ui/patient_visits/visit_1_home.html', ordered_list=ordered_list, search_form=search_form)


class Visit1Form(FlaskForm):
    patient_details = RadioField('Patient')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]



@blueprint.route('/add_visit_1', methods=['GET', 'POST'])
def add_visit_1():
    visit_1_form = Visit1Form()
    if visit_1_form .validate_on_submit():
        visit_1_added =PatientVisit1(
        fit_received_vis_1= visit_1_form.fit_received_vis_1.data,
        patient_details_id= visit_1_form.patient_details .data,
        )
        db.session.add(visit_1_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=visit_1_form , title="Add Visit 1", url=url_for("ui.add_visit_1"))

class BloodVisit1Form(FlaskForm):
    bloods_received_vis_1 = DateField("Date Blood received", format='%Y-%m-%d')


@blueprint.route('/add_blood_received_vis_1/<int:id>', methods=['GET', 'POST'])
def add_blood_received_vis_1(id):
    find_record = db.get_or_404(PatientVisit1,id)
    prev_blood_received = find_record.bloods_received_vis_1
    add_blood_received_form_1 = BloodVisit1Form (bloods_received_vis_1 = prev_blood_received )
    if add_blood_received_form_1 .validate_on_submit():
        find_record.bloods_received_vis_1= add_blood_received_form_1.bloods_received_vis_1.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_blood_received_form_1, id=id, title="Add blood received", url=url_for("ui.add_blood_received_vis_1",id=id))

class FitVisit1Form(FlaskForm):
    fit_received_vis_1 = DateField("Date FIT received", format='%Y-%m-%d')


@blueprint.route('/add_fit_received_vis_1/<int:id>', methods=['GET', 'POST'])
def add_fit_received_vis_1(id):
    find_record = db.get_or_404(PatientVisit1,id)
    prev_fit_received = find_record.fit_received_vis_1
    add_fit_received_form_1 = FitVisit1Form (fit_received_vis_1 = prev_fit_received)
    if add_fit_received_form_1.validate_on_submit():
        find_record.bloods_received_vis_1= add_fit_received_form_1.fit_received_vis_1.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_fit_received_form_1, id=id, title="Add FIT received", url=url_for("ui.add_fit_received_vis_1",id=id))

@blueprint.route('/delete_visit_1/<int:id>', methods=['GET', 'POST'])
def delete_visit_1(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PatientVisit1).where(PatientVisit1.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.visit_1'))
    return render_template('ui/patient_visits/delete_visit_1.html', id=id)


class EditVisit1Form(FlaskForm):
    fit_received_vis_1 = DateField("Date FIT received", format='%Y-%m-%d')
    bloods_received_vis_1 = DateField("Date Blood received", format='%Y-%m-%d')
    patient_details = RadioField('Patient')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]

@blueprint.route('/edit_visit_1/<int:id>', methods=['GET', 'POST'])
def edit_visit_1(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PatientVisit1).where(PatientVisit1.id == edit_id)).scalar()
        prev_fit_received_vis_1 = query_edit.fit_received_vis_1
        prev_bloods_received_vis_1  = query_edit.bloods_received_vis_1
        prev_patient_details_id = query_edit.patient_details_id
        
        ed_form=EditVisit1Form(fit_received_vis_1=prev_fit_received_vis_1, bloods_received_vis_1=prev_bloods_received_vis_1, patient_details=prev_patient_details_id) 

    
    if ed_form.validate_on_submit():
            query_edit.fit_received_vis_1= ed_form.fit_received_vis_1.data
            query_edit.bloods_received_vis_1= ed_form.bloods_received_vis_1.data
            query_edit.patient_details_id = ed_form.patient_details.data 
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html',form = ed_form, id=id, title="Edit Visit 1", url=url_for("ui.edit_visit_1",id=id))