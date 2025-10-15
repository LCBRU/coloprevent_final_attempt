import pytest
from lbrc_flask.pytest.testers import FlaskViewLoggedInTester, RequiresLoginGetTester, PagedResultSet, PageContentAsserter, TableContentAsserter, SearchModalContentAsserter, HtmlPageContentAsserter


class PackShipmentAddPackResultsTester:
    @property
    def endpoint(self):
        return 'ui.search_pack_search_results'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters['shipment_id'] = self.existing_pack_shipment.id


class TestPackShipmentAddPackResults(PackShipmentAddPackResultsTester, FlaskViewLoggedInTester):
    @pytest.mark.parametrize("item_count", PagedResultSet.test_page_edges())
    @pytest.mark.parametrize("current_page", PagedResultSet.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        packs = self.faker.pack().get_list_in_db(item_count=item_count, pack_shipment=None)
        packs = sorted(packs, key=lambda x: (x.pack_identity, x.id))

        self.parameters['page'] = current_page

        resp = self.get()

        paged_result_set = PagedResultSet(page=current_page, expected_results=packs)

        PageContentAsserter(
            url=self.url(external=False),
            paged_result_set=paged_result_set,
        ).assert_all(resp)

        TableContentAsserter(
            result_set=paged_result_set,
        ).assert_all(resp)


class TestPackShipmentAddPackResultsRequiresLogin(PackShipmentAddPackResultsTester, RequiresLoginGetTester):
    ...
