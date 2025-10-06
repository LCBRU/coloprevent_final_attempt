import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskViewLoggedInTester, ModalContentAsserter, ModalFormErrorContentAsserter
from lbrc_flask.pytest.asserts import assert__refresh_response
from lbrc_flask.pytest.form_tester import FormTesterField
from sqlalchemy import select
from coloprevent.model import PackType
from lbrc_flask.database import db
from tests.ui.views.pack_type import PackTypeFormTester, PackTypeViewTester


class SiteEditViewTester(PackTypeViewTester):
    @property
    def endpoint(self):
        return 'ui.edit_packtype'

    @pytest.fixture(autouse=True)
    def set_original_site(self, client, faker):
        self.existing_site = faker.packtype().get_in_db(
            packtype_name='Original Site',
        )
        self.parameters['id'] = self.existing_site.id


class TestSiteEditRequiresLogin(SiteEditViewTester, RequiresLoginGetTester):
    ...


class TestSiteEditGet(SiteEditViewTester, FlaskViewLoggedInTester):
    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get()

        PackTypeFormTester(has_csrf=True).assert_all(resp)


class TestSiteEditPost(SiteEditViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        expected = self.item_creator.get()
        resp = self.post_object(expected)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(PackType)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", PackTypeFormTester().mandatory_fields_edit,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        PackTypeFormTester().assert_all(resp)
        ModalContentAsserter().assert_all(resp)
        ModalFormErrorContentAsserter().assert_missing_required_field(resp, missing_field.field_title)

        self.assert_db_count(1)

    @pytest.mark.parametrize(
        "invalid_column", PackTypeFormTester().string_fields,
    )
    def test__post__invalid_column__string_length(self, invalid_column: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[invalid_column.field_name] = 'A'*1000

        resp = self.post(data)

        PackTypeFormTester().assert_all(resp)
        ModalContentAsserter().assert_all(resp)
        ModalFormErrorContentAsserter().assert__error__string_too_long(resp, invalid_column.field_title)

        self.assert_db_count(1)
