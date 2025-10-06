import pytest
from lbrc_flask.pytest.testers import FlaskViewLoggedInTester, RequiresLoginGetTester, PageCountHelper, PageContentAsserter, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter


class PackIndexTester:
    @property
    def endpoint(self):
        return 'ui.pack'


class TestPackIndex(PackIndexTester, FlaskViewLoggedInTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        packs = self.faker.pack().get_list_in_db(item_count=item_count)
        packs = sorted(packs, key=lambda x: (x.pack_expiry, x.id))

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

        SearchContentAsserter().assert_all(resp)
        HtmlPageContentAsserter(loggedin_user=self.loggedin_user).assert_all(resp)


class TestSiteIndexRequiresLogin(PackIndexTester, RequiresLoginGetTester):
    ...
