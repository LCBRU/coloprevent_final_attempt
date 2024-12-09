from sqlalchemy import String, Integer
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date




class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # back_up_contact:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # site_primary_contact: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # site_code:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class PackTypes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(nullable=False)
    


class PackShipments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    pack_ids: Mapped[int] = mapped_column(nullable=False, unique=True)
    pack_expiry:Mapped[date] = mapped_column(nullable=False)
    addressee:Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted:Mapped[date] = mapped_column( nullable=False)
    date_recieved:Mapped[date] = mapped_column( nullable=False)
    next_due:Mapped[date] = mapped_column( nullable=False)

class PackId(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    pack_ids: Mapped[int] = mapped_column(nullable=False, unique=True)


    
class Packs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    pack_id:Mapped[int] = mapped_column(index=True) 
    expiry:Mapped[date]= mapped_column
   
    
