import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from lbrc_flask.pytest.form_tester import FormTesterField
from sqlalchemy import select
from coloprevent.model import Pack
from lbrc_flask.database import db
from tests.ui.views.pack import PackViewTester


class PackAddViewTester(PackViewTester):
    @property
    def endpoint(self):
        return 'ui.add_pack'

    @pytest.fixture(autouse=True)
    def set_(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes


class TestPackAddRequiresLogin(PackAddViewTester, RequiresLoginGetTester):
    ...


class TestPackAddGet(PackAddViewTester, FlaskFormGetViewTester):
    ...

class TestPackAddPost(PackAddViewTester, FlaskPostViewTester):
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
        "missing_field", PackAddViewTester.fields().mandatory_fields_add,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get(packtype=None, pack_shipment=None, pack_action=None)
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(0)
