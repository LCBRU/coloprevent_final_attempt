import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginGetTester


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


class TestSiteIndex(SiteIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", IndexTester.page_edges())
    def test__get__no_filters(self, item_count):
        self.faker.site().get_list_in_db(item_count=item_count)
        self.get_and_assert_standards(expected_count=item_count)


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginGetTester):
    ...
