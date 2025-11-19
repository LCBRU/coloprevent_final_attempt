import pytest
from lbrc_flask.pytest.testers import FlaskViewLoggedInTester, RequiresLoginTester, SearchModalContentAsserter


class PackShipmentAddPackSearchTester:
    @property
    def endpoint(self):
        return 'ui.search_pack'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters['id'] = self.existing_pack_shipment.id


class TestPackShipmentAddPackSearch(PackShipmentAddPackSearchTester, FlaskViewLoggedInTester):
    def test__get__assert_standards(self):
        resp = self.get()

        SearchModalContentAsserter().assert_all(resp)


class TestPackShipmentAddPackSearchRequiresLogin(PackShipmentAddPackSearchTester, RequiresLoginTester):
    ...
