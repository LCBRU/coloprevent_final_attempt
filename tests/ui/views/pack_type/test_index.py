import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginGetTester, PagedResultSet, SearchContentAsserter, HtmlPageContentAsserter, TableContentAsserter


class SitePackTypeTester:
    @property
    def endpoint(self):
        return 'ui.packtype_home'


class TestPackTypeIndex(SitePackTypeTester, IndexTester):
    @pytest.mark.parametrize("item_count", PagedResultSet.test_page_edges())
    @pytest.mark.parametrize("current_page", PagedResultSet.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        pack_types = self.faker.packtype().get_list_in_db(item_count=item_count)
        pack_types = sorted(pack_types, key=lambda x: (x.id))

        self.parameters['page'] = current_page

        resp = self.get()

        self.assert_all(
            page_count_helper=PagedResultSet(page=current_page, expected_results=pack_types),
            resp=resp,
        )


class TestSiteIndexRequiresLogin(SitePackTypeTester, RequiresLoginGetTester):
    ...
