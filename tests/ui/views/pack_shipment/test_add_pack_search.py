import pytest
from lbrc_flask.pytest.testers import SearchModalTester, RequiresLoginGetTester, ResultHtmlType


class PackShipmentAddPackSearchTester:
    @property
    def endpoint(self):
        return 'ui.search_pack'

    @property
    def result_html_type(self):
        return ResultHtmlType.MODAL

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters['id'] = self.existing_pack_shipment.id


class TestPackShipmentAddPackSearch(PackShipmentAddPackSearchTester, SearchModalTester):
    def test__get__no_filters(self):
        self.get_and_assert_standards()


class TestPackShipmentAddPackSearchRequiresLogin(PackShipmentAddPackSearchTester, RequiresLoginGetTester):
    ...
