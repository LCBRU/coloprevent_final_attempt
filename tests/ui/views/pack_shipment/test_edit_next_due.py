import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester
from lbrc_flask.pytest.asserts import assert__refresh_response, assert__input_date
from lbrc_flask.pytest.form_tester import FormTester, FormTesterDateField
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentEditNextDueViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.add_shipment_next_due'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters = dict(id=self.existing_pack_shipment.id)

    @staticmethod
    def fields() -> FormTester:
        return FormTester([
            FormTesterDateField(
                field_name='next_due',
                field_title='Next Due',
            ),
        ])

    def assert_form(self, resp):
        options = {s.site_name: str(s.id) for s in self.standard_sites}

        assert__input_date(resp.soup, 'next_due')


class TestPackShipmentEditNextDueRequiresLogin(PackShipmentEditNextDueViewTester, RequiresLoginGetTester):
    ...


class TestPackShipmentEditNextDueGet(PackShipmentEditNextDueViewTester, FlaskFormGetViewTester):
    ...


class TestPackShipmentEditNextDuePost(PackShipmentEditNextDueViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get(site=None)
        data = self.get_data_from_object(expected)

        resp = self.post(data)

        assert__refresh_response(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(expected, actual)
