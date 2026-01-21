import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester, ModalContentAsserter, ModalFormErrorContentAsserter
from lbrc_flask.pytest.form_tester import FormTesterField
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import Pack
from lbrc_flask.database import db
from tests.ui.views.pack import PackFormTester, PackViewTester


class PackEditViewTester(PackViewTester):
    @property
    def endpoint(self):
        return 'ui.edit_pack'

    @pytest.fixture(autouse=True)
    def set_original_pack(self, client, faker, set_standard_packages):
        self.existing_pack = faker.pack().get(save=True, packtype=self.standard_packtypes[1], pack_shipment=None, pack_action=None)
        self.parameters['id'] = self.existing_pack.id


class TestPackEditRequiresLogin(PackEditViewTester, RequiresLoginTester):
    ...


class TestPackEditGet(PackEditViewTester, FlaskViewLoggedInTester):
    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get()

        packtype_options = {pt.packtype_name: str(pt.id) for pt in self.standard_packtypes}
        PackFormTester(packtype_options, has_csrf=True).assert_all(resp)


class TestPackEditPost(PackEditViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        expected = self.item_creator.get(save=False, packtype=None, pack_shipment=None, pack_action=None)
        expected.packtype_id = self.standard_packtypes[0].id
        data = self.get_data_from_object(expected)
        data['pack_type'] = str(expected.packtype_id)

        resp = self.post(data)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(Pack)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", PackFormTester().mandatory_fields_edit,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get(save=False,packtype=None, pack_shipment=None, pack_action=None)
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        packtype_options = {pt.packtype_name: str(pt.id) for pt in self.standard_packtypes}
        PackFormTester(packtype_options).assert_all(resp)
        ModalContentAsserter().assert_all(resp)
        ModalFormErrorContentAsserter().assert_missing_required_field(resp, missing_field.field_title)

        self.assert_db_count(1)
