import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskGetViewTester, FlaskPostViewTester, ModelTesterField, ModelTesterField_DataType, ModelTesterFields
from lbrc_flask.pytest.asserts import assert__input_text, assert__input_textarea, assert_csrf_token, assert__refresh_response, assert__error__string_too_long__modal
from sqlalchemy import select
from coloprevent.model import Site
from lbrc_flask.database import db
from tests.ui.views.site.asserts import assert_actual_equals_expected__site, assert_db_count__site


class SiteTester:
    @staticmethod
    def fields() -> ModelTesterFields:
        return ModelTesterFields([
            ModelTesterField(
                field_name='site_name',
                field_title='Site name',
                data_type=ModelTesterField_DataType.STRING,
                is_mandatory=True,
            ),
            ModelTesterField(
                field_name='site_primary_contact',
                field_title='Primary Contact',
                data_type=ModelTesterField_DataType.TEXT,
            ),
            ModelTesterField(
                field_name='site_backup_contact',
                field_title='Back up Contact',
                data_type=ModelTesterField_DataType.TEXT,
            ),
            ModelTesterField(
                field_name='site_code',
                field_title='Site Code',
                data_type=ModelTesterField_DataType.STRING,
                is_mandatory=True,
            ),
        ])

    @property
    def is_modal(self):
        return True

    @property
    def endpoint(self):
        return 'ui.add'

    def assert_form(self, resp):
        assert__input_text(resp.soup, 'site_name')
        assert__input_textarea(resp.soup, 'site_primary_contact')
        assert__input_textarea(resp.soup, 'site_backup_contact')
        assert__input_text(resp.soup, 'site_code')


class TestSiteIndexRequiresLogin(SiteTester, RequiresLoginTester):
    ...


class TestSiteAdd(SiteTester, FlaskGetViewTester):
    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get_and_assert_standards()
        assert_csrf_token(resp.soup)
        self.assert_form(resp)


class TestSiteAdd(SiteTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected: Site = self.faker.site().get()

        resp = self.post_object(expected)

        assert__refresh_response(resp)
        assert_db_count__site(1)

        actual = db.session.execute(select(Site)).scalar()

        assert_actual_equals_expected__site(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", SiteTester.fields().mandatory_fields,
    )
    def test__post__missing_mandatory_field(self, missing_field: ModelTesterField):
        expected: Site = self.faker.site().get()
        data = self.get_data_from_object(expected, skip_fields=[missing_field.field_name])

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert__error__required_field(resp, missing_field.field_title)
        assert_db_count__site(0)


    @pytest.mark.parametrize(
        "invalid_column", SiteTester.fields().string_fields,
    )
    def test__post__invalid_column__string_length(self, invalid_column: ModelTesterField):
        expected: Site = self.faker.site().get()
        data = self.get_data_from_object(expected)
        data[invalid_column.field_name] = 'A'*1000

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        assert_db_count__site(0)
        assert__error__string_too_long__modal(resp.soup, invalid_column.field_title)
