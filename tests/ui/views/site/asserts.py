from sqlalchemy import func, select
from coloprevent.model import Site
from lbrc_flask.database import db


def assert_actual_equals_expected__site(expected: Site, actual: Site):
    assert actual is not None
    assert expected is not None

    assert actual.site_name == expected.site_name
    assert actual.site_primary_contact == actual.site_primary_contact
    assert actual.site_backup_contact == actual.site_backup_contact
    assert actual.site_code == actual.site_code


def assert_db_count__site(expected_count):
    assert db.session.execute(select(func.count(Site.id))).scalar() == expected_count
