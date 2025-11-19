import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from tests.ui.views.pack_type import PackTypeViewTester


class SiteDeleteViewTester(PackTypeViewTester):
    @property
    def request_method(self):
        return self.post

    @property
    def endpoint(self):
        return 'ui.delete_packtype'

    @pytest.fixture(autouse=True)
    def set_existing_item(self, client, faker):
        self.existing_packtype = faker.packtype().get_in_db(
            packtype_name='Original Pack Type',
        )
        self.parameters['id'] = self.existing_packtype.id


class TestSiteDeleteRequiresLogin(SiteDeleteViewTester, RequiresLoginTester):
    ...


class TestSiteDeletePost(SiteDeleteViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(0)

    def test__post__id_valid(self):
        self.parameters['id'] = self.existing_packtype.id + 1
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(1)
