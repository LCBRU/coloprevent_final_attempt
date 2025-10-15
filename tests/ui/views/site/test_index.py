import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginGetTester, PageCountHelper, PageContentAsserter, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


class TestSiteIndex(SiteIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", PageCountHelper.test_page_edges())
    @pytest.mark.parametrize("current_page", PageCountHelper.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        sites = self.faker.site().get_list_in_db(item_count=item_count)
        sites = sorted(sites, key=lambda x: (x.site_name))

        self.parameters['page'] = current_page

        resp = self.get()

        self.assert_all(
            page_count_helper=PageCountHelper(page=current_page, results_count=len(sites)),
            expected_results=sites,
            resp=resp,
        )


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginGetTester):
    ...
