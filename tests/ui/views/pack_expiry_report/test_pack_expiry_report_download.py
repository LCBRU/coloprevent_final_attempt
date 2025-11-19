from lbrc_flask.pytest.testers import RequiresLoginTester


class PackExpiryReportDownloadTester:
    @property
    def endpoint(self):
        return 'ui.pack_expiry_report_download'


class TestPackExpiryReportDoenloadRequiresLogin(PackExpiryReportDownloadTester, RequiresLoginTester):
    ...
