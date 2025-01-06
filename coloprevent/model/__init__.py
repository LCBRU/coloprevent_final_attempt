from sqlalchemy import String, Integer, ForeignKey
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date




class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    back_up_contact:Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    site_primary_contact: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    site_code:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pack_shipments: Mapped[list["PackShipments"]] = relationship(back_populates="site_id") #adding back refernce to packshipments connection


class PackTypes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(nullable=False)
    


class PackShipments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    site_id = Mapped[int] = mapped_column(ForeignKey("site.id")) #attempting to add site fk
    pack_ids: Mapped[int] = mapped_column(nullable=False, unique=True)
    pack_expiry:Mapped[date] = mapped_column(nullable=False)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_recieved:Mapped[date] = mapped_column( nullable=False)
    next_due:Mapped[date] = mapped_column( nullable=False)
    site: Mapped["Site"] = relationship(back_populates="pack_shipments") #adding backreference to site connection 



    
class Packs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_id:Mapped[int] = mapped_column(index=True) 
    expiry:Mapped[date]= mapped_column
   