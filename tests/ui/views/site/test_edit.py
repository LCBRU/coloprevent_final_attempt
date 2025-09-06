import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskPostViewTester, FlaskFormGetViewTester
from lbrc_flask.pytest.asserts import assert__refresh_response, assert__error__string_too_long__modal
from lbrc_flask.pytest.form_tester import FormTesterField
from sqlalchemy import select
from coloprevent.model import Site
from lbrc_flask.database import db
from tests.ui.views.site import SiteFormTester, SiteViewTester


class SiteEditViewTester(SiteViewTester):
    @property
    def endpoint(self):
        return 'ui.edit'

    @pytest.fixture(autouse=True)
    def set_original_site(self, client, faker):
        self.existing_site = faker.site().get_in_db(
            site_name='Original Site',
            site_primary_contact='Original Primary Contact',
            site_backup_contact='Original Backup Contact',
            site_code='Original Site Code',
        )
        self.parameters = dict(id=self.existing_site.id)


class TestSiteEditRequiresLogin(SiteEditViewTester, RequiresLoginGetTester):
    ...


class TestSiteEditGet(SiteEditViewTester, FlaskFormGetViewTester):
    ...


class TestSiteEditPost(SiteEditViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get()
        resp = self.post_object(expected)

        assert__refresh_response(resp)
        self.assert_db_count(1)

        actual = db.session.execute(select(Site)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", SiteFormTester().mandatory_fields_edit,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp.soup)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(1)

    @pytest.mark.parametrize(
        "invalid_column", SiteFormTester().string_fields,
    )
    def test__post__invalid_column__string_length(self, invalid_column: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[invalid_column.field_name] = 'A'*1000

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp.soup)
        self.assert_db_count(1)
        assert__error__string_too_long__modal(resp.soup, invalid_column.field_title)
