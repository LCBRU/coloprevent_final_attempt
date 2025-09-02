import pytest
from lbrc_flask.pytest.testers import RequiresLoginPostTester, FlaskPostViewTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentDeleteViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.delete_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters = dict(id=self.existing_pack_shipment.id)


class TestSiteDeleteRequiresLogin(PackShipmentDeleteViewTester, RequiresLoginPostTester):
    ...


class TestSiteDeletePost(PackShipmentDeleteViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(0)

    def test__post__id_invalid(self):
        resp = self.post(parameters=dict(id=self.existing_pack_shipment.id + 1))

        assert__refresh_response(resp)
        self.assert_db_count(1)
