import pytest
from lbrc_flask.pytest.testers import ResultsTester, RequiresLoginGetTester, PageCountHelper, PageContentAsserter, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


class TestSiteIndex(SiteIndexTester, ResultsTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        sites = self.faker.site().get_list_in_db(item_count=item_count)
        sites = sorted(sites, key=lambda x: (x.site_name))

        self.parameters['page'] = current_page

        resp = self.get()

        page_count_helper = PageCountHelper(page=current_page, results_count=len(sites))

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
                expected_results=page_count_helper.get_current_page_from_results(sites),
                expected_result_count=page_count_helper.expected_results_on_current_page,
            ).assert_all(resp)

        SearchContentAsserter().assert_all(resp)
        HtmlPageContentAsserter(loggedin_user=self.loggedin_user).assert_all(resp)


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginGetTester):
    ...
