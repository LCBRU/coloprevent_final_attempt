from sqlalchemy import String, Integer, ForeignKey
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date




class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    site_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_backup_contact:Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    site_primary_contact: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_code:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pack_shipment: Mapped[list["PackShipment"]] = relationship(back_populates="site") 
    


class PackType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    packtype_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    pack:Mapped[list["Pack"]] = relationship(back_populates="packtype") 

   
    
class Pack(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_identity:Mapped[str] = mapped_column(nullable=False, unique=True)
    pack_expiry:Mapped[date]= mapped_column(nullable=False)
    packtype: Mapped['PackType']=relationship(back_populates=('pack'))
    packtype_id:Mapped[int]=mapped_column(ForeignKey("pack_type.id"))
    pack_shipment: Mapped[list["PackShipment"]] = relationship(back_populates="pack") 
  
    


class PackShipment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_received:Mapped[date] = mapped_column( nullable=False)
    next_due:Mapped[date] = mapped_column( nullable=False)
    site: Mapped["Site"] = relationship(back_populates="pack_shipment") 
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id")) 
    pack: Mapped["Pack"] = relationship(back_populates="pack_shipment") 
    pack_id:  Mapped[int] = mapped_column(ForeignKey("pack.id")) 

#.............................................................................Consumables..............................................
class Consumable(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    consumable_name: Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    cons_details: Mapped[list["ConsumableDetails"]] = relationship(back_populates="cons_name")
    cons_estimates: Mapped[list["ConsumableEstimates"]] = relationship(back_populates="cons_name")
    cons_packs: Mapped[list["ConsumablePacks"]] = relationship(back_populates="cons_name")

class ConsumableDetails(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    cat_no:Mapped[str] = mapped_column(unique=True, nullable=False) # looks alpa-numeric from spreadsheet 
    supplier: Mapped[str]=mapped_column(nullable=False)
    price_increase:Mapped[int]=mapped_column(nullable=True)
    price:Mapped[float]=mapped_column(nullable=False)
    quantity_per_pack:Mapped[int]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_details")
    cons_estimates: Mapped[list["ConsumableEstimates"]] = relationship(back_populates="cons_details")


class ConsumableEstimates(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    est_number_consumables:Mapped[int]=mapped_column(nullable=False)
    est_packs_study: Mapped[int]=mapped_column(nullable=False)
    est_cost:Mapped[float]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_estimates")
    cons_details_id:Mapped[int]=mapped_column(ForeignKey("consumable_details.id"))
    cons_details:Mapped["ConsumableDetails"]=relationship(back_populates="cons_estimates")


class ConsumablePacks(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    date_received:Mapped[date]=mapped_column(nullable=False)
    cost:Mapped[float]=mapped_column(nullable=False)
    number_of_packs:Mapped[int]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable.id"))
    cons_name:Mapped["Consumable"]= relationship(back_populates="cons_packs")
   

   #....................................Visit tables...................................................................................

class PatientDetails(db.Model):
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


class PatientVisit1(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_1:Mapped[date] = mapped_column(nullable=True)
    bloods_received_vis1:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_1")

class PatientVisit4(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_4:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_4")

class PatientVisit5(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_5:Mapped[date] = mapped_column(nullable=True)
    bloods__received_vis_5:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_5")

class PatientVisit6(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_6:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_6")

class PatientVisit7(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    bloods_received_vis_7:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_7")

class PatientVisit9(db.Model):
    id: Mapped[int] =mapped_column(primary_key=True)
    fit_received_vis_9:Mapped[date] = mapped_column(nullable=True)
    bloods_received_vis_9:Mapped[date] = mapped_column(nullable=True)
    patient_details_id: Mapped[int] = mapped_column(ForeignKey("patient_details.id"))
    patient_details:Mapped["PatientDetails"]= relationship(back_populates="visit_9")