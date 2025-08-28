from sqlalchemy import func, select
from coloprevent.model import Site
from lbrc_flask.database import db
from lbrc_flask.pytest.asserts import assert__input_text, assert__input_textarea
from lbrc_flask.pytest.testers import ModelTesterField, ModelTesterField_DataType, ModelTesterFields


class SiteViewTester:
    @property
    def item_creator(self):
        return self.faker.site()

    def assert_db_count(self, expected_count):
        assert db.session.execute(select(func.count(Site.id))).scalar() == expected_count

    def assert_actual_equals_expected(self, expected: Site, actual: Site):
        assert actual is not None
        assert expected is not None

        assert actual.site_name == expected.site_name
        assert actual.site_primary_contact == actual.site_primary_contact
        assert actual.site_backup_contact == actual.site_backup_contact
        assert actual.site_code == actual.site_code

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

    def assert_form(self, resp):
        assert__input_text(resp.soup, 'site_name')
        assert__input_textarea(resp.soup, 'site_primary_contact')
        assert__input_textarea(resp.soup, 'site_backup_contact')
        assert__input_text(resp.soup, 'site_code')
