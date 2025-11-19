import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from tests.ui.views.pack import PackViewTester


class PackDeleteViewTester(PackViewTester):
    @property
    def request_method(self):
        return self.post

    @property
    def endpoint(self):
        return 'ui.delete_pack'

    @pytest.fixture(autouse=True)
    def set_standard_packages(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes

    @pytest.fixture(autouse=True)
    def set_original_pack(self, client, faker, set_standard_packages):
        self.existing_pack = faker.pack().get_in_db(packtype=self.standard_packtypes[1], pack_shipment=None, pack_action=None)
        self.parameters['id'] = self.existing_pack.id


class TestSiteDeleteRequiresLogin(PackDeleteViewTester, RequiresLoginTester):
    ...


class TestSiteDeletePost(PackDeleteViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(0)

    def test__post__id_invalid(self):
        self.parameters['id'] = self.existing_pack.id + 1
        resp = self.post()

        assert__refresh_response(resp)
        self.assert_db_count(1)
