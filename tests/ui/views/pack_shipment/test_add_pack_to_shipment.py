import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_results
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentAddPackViewTester(PackShipmentViewTester):
    @property
    def request_method(self):
        return self.post

    @property
    def endpoint(self):
        return 'ui.add_pack_to_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_standard_packages(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites, set_standard_packages):
        self.existing_pack_shipment = faker.pack_shipment().get(save=True, site=self.standard_sites[1])
        self.existing_pack = faker.pack().get(save=True, packtype=self.standard_packtypes[1], pack_shipment=None, pack_action=None)
        self.parameters['shipment_id'] = self.existing_pack_shipment.id


class TestPackShipmentAddPackRequiresLogin(PackShipmentAddPackViewTester, RequiresLoginTester):
    ...


class TestPackShipmentAddPackPost(PackShipmentAddPackViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        data = {
            'id': self.existing_pack.id,
        }

        resp = self.post(data)

        assert__refresh_results(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(self.existing_pack_shipment, actual)

        assert len(actual.packs) == 1
        assert actual.packs[0].id == self.existing_pack.id
