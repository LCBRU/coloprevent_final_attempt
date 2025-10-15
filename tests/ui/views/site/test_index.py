import pytest
from lbrc_flask.pytest.testers import FlaskViewLoggedInTester, RequiresLoginGetTester, PageCountHelper, PageContentAsserter, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


class TestSiteIndex(SiteIndexTester, FlaskViewLoggedInTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        sites = self.faker.site().get_list_in_db(item_count=item_count)
        sites = sorted(sites, key=lambda x: (x.site_name))

        self.parameters['page'] = current_page

        resp = self.get()

        page_count_helper = PageCountHelper(page=current_page, results_count=len(sites))

        PageContentAsserter(
            url=self.url(external=False),
            page_count_helper=page_count_helper,
        ).assert_all(resp)

        TableContentAsserter(
            expected_results=page_count_helper.get_current_page_from_results(sites),
            page_count_helper=page_count_helper,
        ).assert_all(resp)

        SearchContentAsserter().assert_all(resp)
        HtmlPageContentAsserter(loggedin_user=self.loggedin_user).assert_all(resp)


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginGetTester):
    ...
