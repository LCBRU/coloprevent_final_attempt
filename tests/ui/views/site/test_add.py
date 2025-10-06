import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskViewLoggedInTester, ModalContentAsserter, ModalFormErrorContentAsserter
from lbrc_flask.pytest.asserts import assert__refresh_response
from lbrc_flask.pytest.form_tester import FormTesterField
from sqlalchemy import select
from coloprevent.model import Site
from lbrc_flask.database import db
from tests.ui.views.site import SiteFormTester, SiteViewTester


class SiteAddViewTester(SiteViewTester):
    @property
    def endpoint(self):
        return 'ui.add'


class TestSiteAddRequiresLogin(SiteAddViewTester, RequiresLoginGetTester):
    ...


class TestSiteAddGet(SiteAddViewTester, FlaskViewLoggedInTester):
    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get()

        SiteFormTester(has_csrf=True).assert_all(resp)


class TestSiteAddPost(SiteAddViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        expected = self.item_creator.get()
        resp = self.post_object(expected)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(Site)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", SiteFormTester().mandatory_fields_add,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        SiteFormTester().assert_all(resp)
        ModalContentAsserter().assert_all(resp)
        ModalFormErrorContentAsserter().assert_missing_required_field(resp, missing_field.field_title)

        self.assert_db_count(0)

    @pytest.mark.parametrize(
        "invalid_column", SiteFormTester().string_fields,
    )
    def test__post__invalid_column__string_length(self, invalid_column: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[invalid_column.field_name] = 'A'*1000

        resp = self.post(data)

        SiteFormTester().assert_all(resp)
        ModalContentAsserter().assert_all(resp)
        ModalFormErrorContentAsserter().assert__error__string_too_long(resp, invalid_column.field_title)

        self.assert_db_count(0)
