import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, IndexUnpaginatedTester


class PackExpiryReportIndexTester:
    @property
    def endpoint(self):
        return 'ui.pack_expiry_report'


class TestPackExpiryReportIndex(PackExpiryReportIndexTester, IndexUnpaginatedTester):
    @pytest.mark.parametrize("item_count", IndexUnpaginatedTester.page_edges())
    def test__get__no_filters(self, item_count):
        self.faker.pack().get_list_in_db(item_count=item_count)
        self.get_and_assert_standards(expected_count=item_count)


class TestPackExpiryReportIndexRequiresLogin(PackExpiryReportIndexTester, RequiresLoginGetTester):
    ...
