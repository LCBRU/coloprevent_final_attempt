from sqlalchemy import func, select
from coloprevent.model import PackType
from lbrc_flask.database import db
from lbrc_flask.pytest.asserts import assert__input_text
from lbrc_flask.pytest.testers import ResultHtmlType
from lbrc_flask.pytest.form_tester import FormTester, FormTesterTextField


class PackTypeViewTester:
    @property
    def item_creator(self):
        return self.faker.packtype()

    def assert_db_count(self, expected_count):
        assert db.session.execute(select(func.count(PackType.id))).scalar() == expected_count

    def assert_actual_equals_expected(self, expected: PackType, actual: PackType):
        assert actual is not None
        assert expected is not None

        assert actual.packtype_name == expected.packtype_name

    @staticmethod
    def fields() -> FormTester:
        return FormTester([
            FormTesterTextField(
                field_name='packtype_name',
                field_title='Name',
                is_mandatory=True,
            ),
        ])

    @property
    def result_html_type(self):
        return ResultHtmlType.MODAL

    def assert_form(self, resp):
        assert__input_text(resp.soup, 'packtype_name')
