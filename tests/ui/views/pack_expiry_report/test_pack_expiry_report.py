import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester, SearchContentAsserter, HtmlPageContentAsserter


class PackExpiryReportIndexTester:
    @property
    def endpoint(self):
        return 'ui.pack_expiry_report'


class TestPackExpiryReportIndex(PackExpiryReportIndexTester, FlaskViewLoggedInTester):
    @pytest.mark.parametrize("item_count", [0, 1, 10, 100])
    def test__get__no_filters(self, item_count):
        packs = self.faker.pack().get_list(save=True, item_count=item_count)

        resp = self.get()

        SearchContentAsserter().assert_all(resp)
        HtmlPageContentAsserter(loggedin_user=self.loggedin_user).assert_all(resp)


class TestPackExpiryReportIndexRequiresLogin(PackExpiryReportIndexTester, RequiresLoginTester):
    ...
