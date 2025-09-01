import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskPostViewTester, FlaskFormGetViewTester, ModelTesterField
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import Pack
from lbrc_flask.database import db
from tests.ui.views.pack import PackViewTester


class PackEditViewTester(PackViewTester):
    @property
    def endpoint(self):
        return 'ui.edit_pack'

    @pytest.fixture(autouse=True)
    def set_standard_packages(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes

    @pytest.fixture(autouse=True)
    def set_original_pack(self, client, faker, set_standard_packages):
        self.existing_pack = faker.pack().get_in_db(packtype=self.standard_packtypes[1], pack_shipment=None, pack_action=None)
        self.parameters = dict(id=self.existing_pack.id)


class TestSiteEditRequiresLogin(PackEditViewTester, RequiresLoginGetTester):
    ...


class TestSiteEditGet(PackEditViewTester, FlaskFormGetViewTester):
    ...


class TestSiteEditPost(PackEditViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get(packtype=None, pack_shipment=None, pack_action=None)
        expected.packtype_id = self.standard_packtypes[0].id
        data = self.get_data_from_object(expected)
        data['pack_type'] = str(expected.packtype_id)

        resp = self.post(data)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(Pack)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", PackEditViewTester.fields().mandatory_fields_edit,
    )
    def test__post__missing_mandatory_field(self, missing_field: ModelTesterField):
        expected = self.item_creator.get(packtype=None, pack_shipment=None, pack_action=None)
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(1)
