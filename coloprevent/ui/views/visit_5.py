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
from coloprevent.model import PatientVisit5, PatientDetails
from flask_wtf import FlaskForm
from lbrc_flask.requests import get_value_from_all_arguments


@blueprint.route('/visit_5', methods=['GET', 'POST'])
def visit_5():
     search_form = SearchForm(search_placeholder='Search screening ID', formdata=request.args) 

     q_list = db.session.execute(db.select(PatientVisit5).order_by(PatientVisit5.id)).scalars()
     ordered_list =[]
     for queried in q_list:
        ordered_list.append(queried)

     if search_form.search.data:
        q = q.where(PatientDetails.screening_id.like(f'%{search_form.search.data}%'))
 
     return render_template('ui/patient_visits/visit_5_home.html', ordered_list=ordered_list, search_form=search_form)

class Visit5Form(FlaskForm):
    patient_details = RadioField('Patient')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]


@blueprint.route('/add_visit_5', methods=['GET', 'POST'])
def add_visit_5():
    visit_5_form = Visit5Form()
    if visit_5_form .validate_on_submit():
        visit_5_added =PatientVisit5(
        patient_details_id= visit_5_form.patient_details.data,
        )
        db.session.add(visit_5_added)
        db.session.commit()
        return refresh_response()
    
    return render_template('lbrc/form_modal.html', form=visit_5_form , title="Add Visit 5", url=url_for("ui.add_visit_5"))


class BloodVisit5Form(FlaskForm):
    bloods_received_vis_5 = DateField("Date Blood received", format='%Y-%m-%d')

@blueprint.route('/add_blood_received_vis_5/<int:id>', methods=['GET', 'POST'])
def add_blood_received_vis_5(id):
    find_record = db.get_or_404(PatientVisit5,id)
    prev_blood_received = find_record.bloods_received_vis_5
    add_blood_received_form_5 = BloodVisit5Form (bloods_received_vis_1 = prev_blood_received )
    if add_blood_received_form_5.validate_on_submit():
        find_record.bloods_received_vis_5= add_blood_received_form_5.bloods_received_vis_5.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_blood_received_form_5, id=id, title="Add blood received", url=url_for("ui.add_blood_received_vis_5",id=id))


class FitVisit5Form(FlaskForm):
    fit_received_vis_5 = DateField("Date FIT received", format='%Y-%m-%d')

@blueprint.route('/add_fit_received_vis_5/<int:id>', methods=['GET', 'POST'])
def add_fit_received_vis_5(id):
    find_record = db.get_or_404(PatientVisit5,id)
    prev_fit_received = find_record.fit_received_vis_5
    add_fit_received_form_5 = FitVisit5Form (fit_received_vis_5 = prev_fit_received)
    if add_fit_received_form_5.validate_on_submit():
        find_record.fit_received_vis_5= add_fit_received_form_5.fit_received_vis_5.data
        db.session.add(find_record)
        db.session.commit()
        return refresh_response()
    return render_template('lbrc/form_modal.html', form = add_fit_received_form_5, id=id, title="Add FIT received", url=url_for("ui.add_fit_received_vis_5",id=id))

@blueprint.route('/delete_visit_5/<int:id>', methods=['GET', 'POST'])
def delete_visit_5(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(PatientVisit5).where(PatientVisit5.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect(url_for('ui.visit_5'))
    return render_template('ui/patient_visits/delete_visit_5.html', id=id)

class EditVisit5Form(FlaskForm):
    patient_details = RadioField('Patient')
    fit_received_vis_5 = DateField("Date FIT received", format='%Y-%m-%d')
    bloods_received_vis_5 = DateField("Date Blood received", format='%Y-%m-%d')
    

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.patient_details.choices=[(pd.id, pd.screening_id) for pd in db.session.execute(select(PatientDetails)).scalars()]

@blueprint.route('/edit_visit_5/<int:id>', methods=['GET', 'POST'])
def edit_visit_5(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(PatientVisit5).where(PatientVisit5.id == edit_id)).scalar()
        prev_fit_received_vis_5 = query_edit.fit_received_vis_5
        prev_bloods_received_vis_5  = query_edit.bloods_received_vis_5
        prev_patient_details_id = query_edit.patient_details_id
        
        ed_form=EditVisit5Form(fit_received_vis_5=prev_fit_received_vis_5, bloods_received_vis_5=prev_bloods_received_vis_5, patient_details=prev_patient_details_id) 

    
    if ed_form.validate_on_submit():
            query_edit.patient_details_id = ed_form.patient_details.data 
            query_edit.fit_received_vis_5= ed_form.fit_received_vis_5.data
            query_edit.bloods_received_vis_5= ed_form.bloods_received_vis_5.data
            db.session.add(query_edit)
            db.session.commit()
            return refresh_response()
        

    return render_template('lbrc/form_modal.html',form = ed_form, id=id, title="Edit Visit 5", url=url_for("ui.edit_visit_5",id=id))

