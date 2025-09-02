import pytest
from lbrc_flask.pytest.testers import SearchResultsModalTester, RequiresLoginGetTester, ResultHtmlType


class PackShipmentAddPackResultsTester:
    @property
    def endpoint(self):
        return 'ui.search_pack_search_results'

    @property
    def result_html_type(self):
        return ResultHtmlType.FRAGMENT

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters = dict(shipment_id=self.existing_pack_shipment.id)


class TestPackShipmentAddPackResults(PackShipmentAddPackResultsTester, SearchResultsModalTester):
    @pytest.mark.parametrize("item_count", SearchResultsModalTester.page_edges())
    def test__get__no_filters(self, item_count):
        self.faker.pack().get_list_in_db(item_count=item_count, pack_shipment=None)
        self.get_and_assert_standards(expected_count=item_count)


class TestPackShipmentAddPackResultsRequiresLogin(PackShipmentAddPackResultsTester, RequiresLoginGetTester):
    ...
