import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskGetViewTester
from lbrc_flask.pytest.asserts import assert__input_text, assert__input_textarea, assert_csrf_token


class TestSiteIndexRequiresLogin(RequiresLoginTester):
    @property
    def endpoint(self):
        return 'ui.add'


class TestSiteAdd(FlaskGetViewTester):
    @property
    def endpoint(self):
        return 'ui.add'

    def assert_form(self, resp):
        assert__input_text(resp.soup, 'site_name')
        assert__input_textarea(resp.soup, 'site_primary_contact')
        assert__input_textarea(resp.soup, 'site_backup_contact')
        assert__input_text(resp.soup, 'site_code')

    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get_modal_and_assert_standards()
        assert_csrf_token(resp.soup)
        self.assert_form(resp)
