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
    pack_shipments: Mapped[list["PackShipments"]] = relationship(back_populates="site") 
    


class PackTypes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    packtype_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    packs:Mapped[list["Packs"]] = relationship(back_populates="packtypes") 

   
    
class Packs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_identity:Mapped[str] = mapped_column(nullable=False, unique=True)
    pack_expiry:Mapped[date]= mapped_column(nullable=False)
    pack_quantity: Mapped[int] = mapped_column(nullable=False)
    packtypes: Mapped['PackTypes']=relationship(back_populates=('packs'))
    packtypes_id:Mapped[int]=mapped_column(ForeignKey("pack_types.id"))
    pack_shipments: Mapped[list["PackShipments"]] = relationship(back_populates="packs") 
  
    


class PackShipments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_received:Mapped[date] = mapped_column( nullable=False)
    next_due:Mapped[date] = mapped_column( nullable=False)
    site: Mapped["Site"] = relationship(back_populates="pack_shipments") 
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id")) 
    packs: Mapped["Packs"] = relationship(back_populates="pack_shipments") 
    pack_id:  Mapped[int] = mapped_column(ForeignKey("packs.id")) 

#.............................................................................Consumables..............................................
class ConsumableName(db.Model):
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
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable_name.id"))
    cons_name:Mapped["ConsumableName"]= relationship(back_populates="cons_details")
    cons_estimates: Mapped[list["ConsumableEstimates"]] = relationship(back_populates="cons_details")
    cons_packs: Mapped[list["ConsumablePacks"]] = relationship(back_populates="cons_details")


class ConsumableEstimates(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    est_number_consumables:Mapped[int]=mapped_column(nullable=False)
    est_packs_study: Mapped[int]=mapped_column(nullable=False)
    est_cost:Mapped[float]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable_name.id"))
    cons_name:Mapped["ConsumableName"]= relationship(back_populates="cons_estimates")
    cons_details_id:Mapped[int]=mapped_column(ForeignKey("consumable_deatils.id"))
    cons_details:Mapped["ConsumableDetails"]=relationship(back_populates="cons_estimates")


class ConsumablePacks(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    date_received:Mapped[date]=mapped_column(nullable=False)
    cost:Mapped[float]=mapped_column(nullable=False)
    number_of_packs:Mapped[int]=mapped_column(nullable=False)
    cons_name_id: Mapped[int] = mapped_column(ForeignKey("consumable_name.id"))
    cons_name:Mapped["ConsumableName"]= relationship(back_populates="cons_packs")
    cons_details_id:Mapped[int]=mapped_column(ForeignKey("consumable_deatils.id"))
    cons_details:Mapped["ConsumableDetails"]=relationship(back_populates="cons_packs")

   