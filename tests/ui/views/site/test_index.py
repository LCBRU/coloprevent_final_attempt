import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginTester, PagedResultSet


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


class TestSiteIndex(SiteIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", PagedResultSet.test_page_edges())
    @pytest.mark.parametrize("current_page", PagedResultSet.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        sites = self.faker.site().get_list_in_db(item_count=item_count)
        sites = sorted(sites, key=lambda x: (x.site_name))

        self.parameters['page'] = current_page

        resp = self.get()

        self.assert_all(
            page_count_helper=PagedResultSet(page=current_page, expected_results=sites),
            resp=resp,
        )


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginTester):
    ...
