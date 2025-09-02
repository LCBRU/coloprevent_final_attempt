import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester, ModelTesterField
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester
from lbrc_flask.pytest.asserts import assert__input_date
from lbrc_flask.pytest.testers import ModelTesterField, ModelTesterField_DataType, ModelTesterFields


class PackShipmentEditDateReceivedViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.add_shipment_received'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters = dict(id=self.existing_pack_shipment.id)

    @staticmethod
    def fields() -> ModelTesterFields:
        return ModelTesterFields([
            ModelTesterField(
                field_name='date_received',
                field_title='Date Received',
                data_type=ModelTesterField_DataType.DATE,
            ),
        ])

    def assert_form(self, resp):
        options = {s.site_name: str(s.id) for s in self.standard_sites}

        assert__input_date(resp.soup, 'date_received')


class TestPackShipmentEditDateReceivedRequiresLogin(PackShipmentEditDateReceivedViewTester, RequiresLoginGetTester):
    ...


class TestPackShipmentEditDateReceivedGet(PackShipmentEditDateReceivedViewTester, FlaskFormGetViewTester):
    ...


class TestPackShipmentEditDateReceivedPost(PackShipmentEditDateReceivedViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get(site=None)
        data = self.get_data_from_object(expected)

        resp = self.post(data)

        assert__refresh_response(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(expected, actual)
