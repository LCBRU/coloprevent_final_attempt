from lbrc_flask.pytest.testers import RequiresLoginGetTester


class PackExpiryReportDownloadTester:
    @property
    def endpoint(self):
        return 'ui.pack_expiry_report_download'


class TestPackExpiryReportDoenloadRequiresLogin(PackExpiryReportDownloadTester, RequiresLoginGetTester):
    ...
