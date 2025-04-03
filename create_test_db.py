#!/usr/bin/env python3

from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()

from lbrc_flask.database import db
from lbrc_flask.security import init_roles, init_users
from alembic.config import Config
from alembic import command
from faker import Faker
from coloprevent.model import *

fake = Faker()

from coloprevent import create_app

application = create_app()
application.app_context().push()
db.create_all()
init_roles([])
init_users()

alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")

# TO DO: Create test data
site_added = Site(
    site_name= "Leicester",
    site_backup_contact = "Test backup",
    site_primary_contact= "Test primary contact",
    site_code = 1)

db.session.add(site_added)
db.session.commit()


packtype_added = PackType(
    packtype_name = "Research bloods"
     
    )

db.session.add(packtype_added)
db.session.commit()


pack_added = Pack(
    packtype_id = packtype_added.id,
    pack_identity = 1,
    pack_expiry = date(2025,3,28),

    
    )
db.session.add(pack_added)
db.session.commit()

pack_shipment_added = PackShipment(
    date_posted = date(2025,3,28),
    date_received = date(2025,3,31),
    next_due = date(2025,4,30),
    site_id = site_added.id
)

db.session.add(pack_shipment_added)
db.session.commit()


db.session.close()


