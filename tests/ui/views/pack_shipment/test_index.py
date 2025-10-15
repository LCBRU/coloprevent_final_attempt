import pytest
from lbrc_flask.pytest.testers import FlaskViewLoggedInTester, RequiresLoginGetTester, PageCountHelper, PageContentAsserter, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter
from lbrc_flask.python_helpers import sort_descending


class PackShipmentIndexTester:
    @property
    def endpoint(self):
        return 'ui.index'


class TestPackShipmentIndex(PackShipmentIndexTester, FlaskViewLoggedInTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        pack_shiptments = self.faker.pack_shipment().get_list_in_db(item_count=item_count)
        pack_shipments = sorted(pack_shiptments, key=lambda x: (sort_descending(x.date_posted), sort_descending(x.id)))

        self.parameters['page'] = current_page

        resp = self.get()

        page_count_helper = PageCountHelper(page=current_page, results_count=len(pack_shipments))

        PageContentAsserter(
            url=self.url(external=False),
            page_count_helper=page_count_helper,
        ).assert_all(resp)

        TableContentAsserter(
            expected_results=page_count_helper.get_current_page_from_results(pack_shipments),
            page_count_helper=page_count_helper,
        ).assert_all(resp)

        SearchContentAsserter().assert_all(resp)
        HtmlPageContentAsserter(loggedin_user=self.loggedin_user).assert_all(resp)


class TestPackShipmentIndexRequiresLogin(PackShipmentIndexTester, RequiresLoginGetTester):
    ...
