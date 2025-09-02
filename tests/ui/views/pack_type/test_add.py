import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester, ModelTesterField
from lbrc_flask.pytest.asserts import assert__refresh_response, assert__error__string_too_long__modal
from sqlalchemy import select
from coloprevent.model import PackType
from lbrc_flask.database import db
from tests.ui.views.pack_type import PackTypeViewTester


class PackTypeAddViewTester(PackTypeViewTester):
    @property
    def endpoint(self):
        return 'ui.add_packtype'


class TestSiteAddRequiresLogin(PackTypeAddViewTester, RequiresLoginGetTester):
    ...


class TestSiteAddGet(PackTypeAddViewTester, FlaskFormGetViewTester):
    ...

class TestSiteAddPost(PackTypeAddViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get()
        resp = self.post_object(expected)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(PackType)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", PackTypeAddViewTester.fields().mandatory_fields_add,
    )
    def test__post__missing_mandatory_field(self, missing_field: ModelTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(0)

    @pytest.mark.parametrize(
        "invalid_column", PackTypeAddViewTester.fields().string_fields,
    )
    def test__post__invalid_column__string_length(self, invalid_column: ModelTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[invalid_column.field_name] = 'A'*1000

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert_db_count(0)
        assert__error__string_too_long__modal(resp.soup, invalid_column.field_title)
