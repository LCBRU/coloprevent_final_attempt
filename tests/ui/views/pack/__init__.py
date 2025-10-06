import pytest
from sqlalchemy import func, select
from coloprevent.model import Pack
from lbrc_flask.database import db
from lbrc_flask.pytest.form_tester import FormTester, FormTesterTextField, FormTesterDateField, FormTesterRadioField


class PackFormTester(FormTester):
    def __init__(self, packtype_options=None, has_csrf=False):
        packtype_options = packtype_options or {}

        super().__init__(
            fields=[
                FormTesterTextField(
                    field_name='pack_identity',
                    field_title='Pack Identity',
                    is_mandatory=True,
                ),
                FormTesterDateField(
                    field_name='pack_expiry',
                    field_title='Pack Expiry',
                    is_mandatory=True,
                ),
                FormTesterRadioField(
                    field_name='pack_type',
                    field_title='Packtype',
                    is_mandatory=True,
                    options=packtype_options,
                ),
            ],
            has_csrf=has_csrf,
        )

    def assert_form(self, soup):
        options = {pt.packtype_name: str(pt.id) for pt in self.standard_packtypes}
        PackFormTester(packtype_options=options).assert_inputs(soup)


class PackViewTester:
    @property
    def item_creator(self):
        return self.faker.pack()

    @pytest.fixture(autouse=True)
    def set_standard_packages(self, standard_packtypes):
        self.standard_packtypes = standard_packtypes

    def assert_db_count(self, expected_count):
        assert db.session.execute(select(func.count(Pack.id))).scalar() == expected_count

    def assert_actual_equals_expected(self, expected: Pack, actual: Pack):
        assert actual is not None
        assert expected is not None

        assert actual.pack_identity == expected.pack_identity
        assert actual.pack_expiry == expected.pack_expiry

        assert actual.packtype_id == expected.packtype_id
        assert (actual.pack_shipment is None) == (expected.pack_shipment is None)
        if actual.pack_shipment is not None:
            assert actual.pack_shipment.id == expected.pack_shipment.id
        assert actual.pack_action == expected.pack_action
