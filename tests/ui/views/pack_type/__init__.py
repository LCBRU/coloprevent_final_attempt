from sqlalchemy import func, select
from coloprevent.model import PackType
from lbrc_flask.database import db
from lbrc_flask.pytest.asserts import assert__input_text
from lbrc_flask.pytest.testers import ModelTesterField, ModelTesterField_DataType, ModelTesterFields


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
    def fields() -> ModelTesterFields:
        return ModelTesterFields([
            ModelTesterField(
                field_name='packtype_name',
                field_title='Name',
                data_type=ModelTesterField_DataType.STRING,
                is_mandatory=True,
            ),
        ])

    @property
    def is_modal(self):
        return True

    def assert_form(self, resp):
        assert__input_text(resp.soup, 'packtype_name')
