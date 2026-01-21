import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import Pack, PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentDeletePackViewTester(PackShipmentViewTester):
    @property
    def request_method(self):
        return self.post

    @property
    def endpoint(self):
        return 'ui.delete_pack_to_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_standard_packages(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites, set_standard_packages):
        self.existing_pack: Pack = faker.pack().get(save=True, packtype=self.standard_packtypes[1], pack_shipment=None, pack_action=None)
        self.existing_pack_shipment: PackShipment = faker.pack_shipment().get(save=True, site=self.standard_sites[1])

        self.existing_pack_shipment.packs.append(self.existing_pack)

        db.session.add(self.existing_pack_shipment)
        db.session.commit()

        self.parameters['id'] = self.existing_pack_shipment.id
        self.parameters['pack_id'] = self.existing_pack.id


class TestPackShipmentDeletePackRequiresLogin(PackShipmentDeletePackViewTester, RequiresLoginTester):
    ...


class TestPackShipmentDeletePackPost(PackShipmentDeletePackViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(self.existing_pack_shipment, actual)

        assert len(actual.packs) == 0
