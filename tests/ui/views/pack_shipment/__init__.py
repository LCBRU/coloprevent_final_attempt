from sqlalchemy import func, select
from coloprevent.model import PackShipment
from lbrc_flask.database import db


class PackShipmentViewTester:
    @property
    def item_creator(self):
        return self.faker.pack_shipment()

    def assert_db_count(self, expected_count):
        assert db.session.execute(select(func.count(PackShipment.id))).scalar() == expected_count

    def assert_actual_equals_expected(self, expected: PackShipment, actual: PackShipment):
        assert actual is not None
        assert expected is not None

        actual.date_posted == expected.date_posted
        actual.date_received == expected.date_received
        actual.next_due == expected.next_due
        actual.site_id == expected.site_id

        actual_pack_ids = sorted([p.id for p in actual.packs])
        expected_pack_ids = sorted([p.id for p in expected.packs])

        assert actual_pack_ids == expected_pack_ids

    @property
    def is_modal(self):
        return True
