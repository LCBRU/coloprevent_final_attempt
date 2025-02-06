#!/usr/bin/env python3

from dotenv import load_dotenv
from lbrc_flask.database import db
from lbrc_flask.security import init_roles, init_users
from alembic.config import Config
from alembic import command
from faker import Faker
from coloprevent.model import *

fake = Faker()

# Load environment variables from '.env' file.
load_dotenv()

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
    site_code = "123ABC")

db.session.add(site_added)
db.session.commit()
db.session.commit()
db.session.close()

