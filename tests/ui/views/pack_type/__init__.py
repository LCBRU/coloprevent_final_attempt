from sqlalchemy import func, select
from coloprevent.model import PackType
from lbrc_flask.database import db
from lbrc_flask.pytest.asserts import assert__input_text
from lbrc_flask.pytest.testers import ResultHtmlType
from lbrc_flask.pytest.form_tester import FormTester, FormTesterTextField


class PackTypeFormTester(FormTester):
    def __init__(self):
        super().__init__(fields=[
            FormTesterTextField(
                field_name='packtype_name',
                field_title='Name',
                is_mandatory=True,
            ),
        ])


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

    @property
    def result_html_type(self):
        return ResultHtmlType.MODAL

    def assert_form(self, soup):
        PackTypeFormTester().assert_inputs(soup)
