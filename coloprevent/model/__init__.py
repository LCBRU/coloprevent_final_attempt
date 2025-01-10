from sqlalchemy import String, Integer, ForeignKey
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date




class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    site_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_back_up_contact:Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    site_primary_contact: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_code:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pack_shipments: Mapped[list["PackShipments"]] = relationship(back_populates="site") 
    packs: Mapped[list["Packs"]]= relationship(back_populates='site')


class PackTypes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    packtype_name: Mapped[str] = mapped_column(nullable=False)
    packs:Mapped[list["Packs"]] = relationship(back_populates="packtypes") 

   
    
class Packs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_identity:Mapped[int] = mapped_column(nullable=False)
    pack_expiry:Mapped[date]= mapped_column(nullable=False)
    pack_quantity: Mapped[int] = mapped_column(nullable=False)
    site: Mapped['Site']=relationship(back_populates='packs')
    site_id: Mapped[int]= mapped_column(ForeignKey("site.id"))
    packtypes: Mapped['PackTypes']=relationship(back_populates=('packs'))
    packtypes_id:Mapped[int]=mapped_column(ForeignKey("pack_types.id"))
  
    


class PackShipments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_recieved:Mapped[date] = mapped_column( nullable=False)
    next_due:Mapped[date] = mapped_column( nullable=False)
    site: Mapped["Site"] = relationship(back_populates="pack_shipments") 
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id")) 




    

   