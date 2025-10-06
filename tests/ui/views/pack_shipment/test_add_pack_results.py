import pytest
from lbrc_flask.pytest.testers import ResultsTester, RequiresLoginGetTester, ResultHtmlType, PageCountHelper, PageContentAsserter, TableContentAsserter, SearchModalContentAsserter, HtmlPageContentAsserter


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
        self.parameters['shipment_id'] = self.existing_pack_shipment.id


class TestPackShipmentAddPackResults(PackShipmentAddPackResultsTester, ResultsTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        packs = self.faker.pack().get_list_in_db(item_count=item_count, pack_shipment=None)
        packs = sorted(packs, key=lambda x: (x.pack_identity, x.id))

        self.parameters['page'] = current_page

        resp = self.get()

        page_count_helper = PageCountHelper(page=current_page, results_count=len(packs))

        if current_page > page_count_helper.page_count:
            # I can't work out how to limit the number of current pages to the number of
            # actual pages there are going to be!
            pass
        else:
            page_asserter = PageContentAsserter(
                url=self.url(external=False),
                page_count_helper=page_count_helper,
            ).assert_all(resp)

            TableContentAsserter(
                expected_results=page_count_helper.get_current_page_from_results(packs),
                expected_result_count=page_count_helper.expected_results_on_current_page,
            ).assert_all(resp)


class TestPackShipmentAddPackResultsRequiresLogin(PackShipmentAddPackResultsTester, RequiresLoginGetTester):
    ...
