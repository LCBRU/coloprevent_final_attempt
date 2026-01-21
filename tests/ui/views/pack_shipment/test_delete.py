import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentDeleteViewTester(PackShipmentViewTester):
    @property
    def request_method(self):
        return self.post

    @property
    def endpoint(self):
        return 'ui.delete_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get(save=True, site=self.standard_sites[1])
        self.parameters['id'] = self.existing_pack_shipment.id


class TestSiteDeleteRequiresLogin(PackShipmentDeleteViewTester, RequiresLoginTester):
    ...


class TestSiteDeletePost(PackShipmentDeleteViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(0)

    def test__post__id_invalid(self):
        self.parameters['id'] = self.existing_pack_shipment.id + 1
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(1)
