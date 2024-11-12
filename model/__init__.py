from sqlalchemy import String
from lbrc_flask.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date




class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)


    
class Packs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True) 
    #site = Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pack_id:Mapped[int] = mapped_column(primary_key=True)
    expiry:Mapped[date]=mapped_column
   
    


class Consumables(db.Model):
    consumable_id:Mapped[int] = mapped_column(primary_key=True)
    consumable_type:Mapped[str] =mapped_column

