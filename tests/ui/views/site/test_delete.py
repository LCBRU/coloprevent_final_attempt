import pytest
from lbrc_flask.pytest.testers import RequiresLoginPostTester, FlaskPostViewTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from tests.ui.views.site import SiteViewTester


class SiteDeleteViewTester(SiteViewTester):
    @property
    def endpoint(self):
        return 'ui.delete'

    @pytest.fixture(autouse=True)
    def set_existing_site(self, client, faker):
        self.existing_site = faker.site().get_in_db(
            site_name='Original Site',
            site_primary_contact='Original Primary Contact',
            site_backup_contact='Original Backup Contact',
            site_code='Original Site Code',
        )
        self.parameters['id'] = self.existing_site.id


class TestSiteDeleteRequiresLogin(SiteDeleteViewTester, RequiresLoginPostTester):
    ...


class TestSiteDeletePost(SiteDeleteViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(0)

    def test__post__id_valid(self):
        self.parameters['id'] = self.existing_site.id + 1
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(1)
