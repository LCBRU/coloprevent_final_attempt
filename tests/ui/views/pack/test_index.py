import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginTester, PagedResultSet


class PackIndexTester:
    @property
    def endpoint(self):
        return 'ui.pack'


class TestPackIndex(PackIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", PagedResultSet.test_page_edges())
    @pytest.mark.parametrize("current_page", PagedResultSet.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        packs = self.faker.pack().get_list_in_db(item_count=item_count)
        packs = sorted(packs, key=lambda x: (x.pack_expiry, x.id))

        self.parameters['page'] = current_page

        resp = self.get()

        self.assert_all(
            page_count_helper=PagedResultSet(page=current_page, expected_results=packs),
            resp=resp,
        )


class TestSiteIndexRequiresLogin(PackIndexTester, RequiresLoginTester):
    ...
