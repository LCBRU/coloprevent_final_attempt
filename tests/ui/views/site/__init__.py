from sqlalchemy import func, select
from coloprevent.model import Site
from lbrc_flask.database import db
from lbrc_flask.pytest.form_tester import FormTester, FormTesterTextField, FormTesterTextAreaField


class SiteFormTester(FormTester):
    def __init__(self, has_csrf=False):
        super().__init__(
            fields=[
                FormTesterTextField(
                    field_name='site_name',
                    field_title='Site name',
                    is_mandatory=True,
                ),
                FormTesterTextAreaField(
                    field_name='site_primary_contact',
                    field_title='Primary Contact',
                ),
                FormTesterTextAreaField(
                    field_name='site_backup_contact',
                    field_title='Back up Contact',
                ),
                FormTesterTextField(
                    field_name='site_code',
                    field_title='Site Code',
                    is_mandatory=True,
                ),
            ],
            has_csrf=has_csrf,
        )


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
