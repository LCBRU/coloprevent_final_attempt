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
from coloprevent.model import PatientVisit4, PatientDetails
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments


@blueprint.route('/visit_4', methods=['GET', 'POST'])
def visit_4():
     search_form = SearchForm(search_placeholder='Search screening ID', formdata=request.args) 

     q_list = db.session.execute(db.select(PatientVisit4).order_by(PatientVisit4.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)

     if search_form.search.data:
        q = q.where(PatientDetails.screening_id.like(f'%{search_form.search.data}%'))
 
     return render_template('ui/patient_visits/visit_4_home.html', ordered_list=ordered_list, search_form=search_form)

class Visit4Form(FlaskForm):
    patient_details = RadioField('Patient')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]

@blueprint.route('/add_visit_4', methods=['GET', 'POST'])
def add_visit_4():
    visit_4_form = Visit4Form()
    if visit_4_form .validate_on_submit():
        visit_4_added =PatientVisit4(
        patient_details_id= visit_4_form.patient_details .data,
        )
        db.session.add(visit_4_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=visit_4_form , title="Add Visit 1", url=url_for("ui.add_visit_4"))

class BloodVisit4Form(FlaskForm):
    bloods_received_vis_4 = DateField("Date Blood received", format='%Y-%m-%d')

@blueprint.route('/add_blood_received_vis_4/<int:id>', methods=['GET', 'POST'])
def add_blood_received_vis_4(id):
    find_record = db.get_or_404(PatientVisit4,id)
    prev_blood_received = find_record.bloods_received_vis_4
    add_blood_received_form_4 = BloodVisit4Form (bloods_received_vis_4 = prev_blood_received )
    if add_blood_received_form_4.validate_on_submit():
        find_record.bloods_received_vis_4= add_blood_received_form_4.bloods_received_vis_4.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_blood_received_form_4, id=id, title="Add blood received", url=url_for("ui.add_blood_received_vis_4",id=id))

@blueprint.route('/delete_visit_4/<int:id>', methods=['GET', 'POST'])
def delete_visit_4(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PatientVisit4).where(PatientVisit4.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.visit_4'))
    return render_template('ui/patient_visits/delete_visit_4.html', id=id)


class EditVisit4Form(FlaskForm):
    patient_details = RadioField('Patient')
    bloods_received_vis_4 = DateField("Date Blood received", format='%Y-%m-%d')
    

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]


@blueprint.route('/edit_visit_4/<int:id>', methods=['GET', 'POST'])
def edit_visit_4(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PatientVisit4).where(PatientVisit4.id == edit_id)).scalar()
        prev_bloods_received_vis_4  = query_edit.bloods_received_vis_4
        prev_patient_details_id = query_edit.patient_details_id
        
        ed_form=EditVisit4Form(bloods_received_vis_4=prev_bloods_received_vis_4, patient_details=prev_patient_details_id) 

    
    if ed_form.validate_on_submit():
            query_edit.patient_details_id = ed_form.patient_details.data 
            query_edit.bloods_received_vis_4= ed_form.bloods_received_vis_4.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html',form = ed_form, id=id, title="Edit Visit 4", url=url_for("ui.edit_visit_4",id=id))

