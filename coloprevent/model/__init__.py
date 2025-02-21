from sqlalchemy import String, Integer, ForeignKey
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from lbrc_flask.security import AuditMixin 




class Site(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True) 
    site_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_backup_contact:Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    site_primary_contact: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_code:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pack_shipment: Mapped[list["PackShipment"]] = relationship(back_populates="site") 
    


class PackType(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True) 
    packtype_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    packs:Mapped[list["Pack"]] = relationship(back_populates="packtype") 

   
    
class Pack(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_identity:Mapped[int] = mapped_column(nullable=False, unique=True)
    pack_expiry:Mapped[date]= mapped_column(nullable=False)
    packtype: Mapped['PackType']=relationship(back_populates=('packs'))
    packtype_id:Mapped[int]=mapped_column(ForeignKey("pack_type.id"))
    pack_shipment: Mapped["PackShipment"] = relationship(back_populates="packs") 
    pack_shipment_id: Mapped[int] = mapped_column(ForeignKey("pack_shipment.id"), nullable=True)
    expiry_report: Mapped[list["ExpiryReport"]] = relationship(back_populates="pack") #added for report test
    @property
    def name(self):
        return f'{self.packtype.packtype_name}: {self.pack_identity}'

    
    



class PackShipment(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_received:Mapped[date] = mapped_column( nullable=True)
    next_due:Mapped[date] = mapped_column( nullable=True)
    site: Mapped["Site"] = relationship(back_populates="pack_shipment") 
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id")) 
    packs:Mapped[list["Pack"]] = relationship(back_populates="pack_shipment")
    expiry_report: Mapped[list["ExpiryReport"]] = relationship(back_populates="pack_shipment") 

    

class ExpiryReport(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(ForeignKey("pack.id"))
    pack: Mapped["Pack"] = relationship(back_populates="expiry_report")
    pack_shipment_id:Mapped[int] = mapped_column(ForeignKey("pack_shipment.id"))
    pack_shipment: Mapped["PackShipment"] = relationship(back_populates="expiry_report")
  
     

    
    

   

#.............................................................................Consumables..............................................
class Consumable(db.Model,AuditMixin ):
    id: Mapped[int] = mapped_column(primary_key=True)
    consumable_name: Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    cons_details: Mapped[list["ConsumableDetails"]] = relationship(back_populates="cons_name")
    cons_estimates: Mapped[list["ConsumableEstimates"]] = relationship(back_populates="cons_name")
    cons_packs: Mapped[list["ConsumablePacks"]] = relationship(back_populates="cons_name")

class ConsumableDetails(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    cat_no:Mapped[str] = mapped_column(unique=True, nullable=False) # looks alpa-numeric from spreadsheet 
    supplier: Mapped[str]=mapped_column(nullable=False)
    price_increase:Mapped[int]=mapped_column(nullable=True)
    price:Mapped[float]=mapped_column(nullable=False)
    quantity_per_pack:Mapped[int]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_details")
    cons_estimates: Mapped[list["ConsumableEstimates"]] = relationship(back_populates="cons_details")


class ConsumableEstimates(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    est_number_consumables:Mapped[int]=mapped_column(nullable=False)
    est_packs_study: Mapped[int]=mapped_column(nullable=False)
    est_cost:Mapped[float]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_estimates")
    cons_details_id:Mapped[int]=mapped_column(ForeignKey("consumable_details.id"))
    cons_details:Mapped["ConsumableDetails"]=relationship(back_populates="cons_estimates")


class ConsumablePacks(db.Model, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    date_received:Mapped[date]=mapped_column(nullable=False)
    cost:Mapped[float]=mapped_column(nullable=False)
    number_of_packs:Mapped[int]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_packs")
   

   #....................................Visit tables...................................................................................

class PatientDetails(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    screening_id: Mapped[str]=mapped_column(nullable=False, unique=True)
    pid:Mapped[str]=mapped_column(nullable=False, unique=True)
    date_of_consent: Mapped[date]=mapped_column(nullable=False)
    visit_1: Mapped[list["PatientVisit1"]] = relationship(back_populates="patient_details")
    visit_4: Mapped[list["PatientVisit4"]] = relationship(back_populates="patient_details")
    visit_5: Mapped[list["PatientVisit5"]] = relationship(back_populates="patient_details")
    visit_6: Mapped[list["PatientVisit6"]] = relationship(back_populates="patient_details")
    visit_7: Mapped[list["PatientVisit7"]] = relationship(back_populates="patient_details")
    visit_9: Mapped[list["PatientVisit9"]] = relationship(back_populates="patient_details")


class PatientVisit1(db.Model,AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_1:Mapped[date] = mapped_column(nullable=True)
    bloods_received_vis_1:Mapped[date] = mapped_column(nullable=True) #correct underscore 
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_1")

class PatientVisit4(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_4:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_4")

class PatientVisit5(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_5:Mapped[date] = mapped_column(nullable=True)
    bloods_received_vis_5:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_5")

class PatientVisit6(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_6:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_6")

class PatientVisit7(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_7:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_7")

class PatientVisit9(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_9:Mapped[date] = mapped_column(nullable=True)
    bloods_received_vis_9:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_9")

    #...................................City Sprint Tracker............................................................................

class CsFrom(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    cs_from: Mapped[str] = mapped_column(nullable=True, unique=True)

class CsSiteCode(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    cs_site_code: Mapped[str] = mapped_column(unique=True, nullable=True)


class CsTo(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    cs_to: Mapped[str] = mapped_column(unique=True, nullable=True)

class CsSentDetails(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    date_logged_citysprint: Mapped[date] = mapped_column(nullable=False)
    citysprint_ref_number: Mapped[int] = mapped_column(nullable=False, unique=True)
    total_cost: Mapped[float] = mapped_column(nullable=False)
    cost: Mapped[float] = mapped_column(nullable=False) #will need to add vat to this 
    packaging: Mapped[str] = mapped_column(nullable=False)
    number_of_aliquots:Mapped[int] = mapped_column(nullable=False)
    storage_logs_available:Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str]= mapped_column(nullable=False)
    scheduled_date_of_receipt:Mapped[date] = mapped_column(nullable=False)

class CsReceivedDetails(db.Model, AuditMixin):
     id: Mapped[int] =mapped_column(primary_key=True)
     date_received: Mapped[date]= mapped_column(nullable=False)
     time_received: Mapped[time]= mapped_column(nullable=False)
     time_freezer: Mapped[time] = mapped_column(nullable=False)
    

class CsRecipient(db.Model, AuditMixin):
    id: Mapped[int] =mapped_column(primary_key=True)
    received_by: Mapped[str] = mapped_column(nullable=False)
    

    




    