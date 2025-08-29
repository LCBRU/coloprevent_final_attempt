import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginGetTester


class PackIndexTester:
    @property
    def endpoint(self):
        return 'ui.pack'


class TestSiteIndex(PackIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", IndexTester.page_edges())
    def test__get__no_filters(self, item_count):
        self.faker.pack().get_list_in_db(item_count=item_count)
        self.get_and_assert_standards(expected_count=item_count)


class TestSiteIndexRequiresLogin(PackIndexTester, RequiresLoginGetTester):
    ...
