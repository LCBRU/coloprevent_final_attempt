from sqlalchemy import func, select
from coloprevent.model import Pack
from lbrc_flask.database import db
from lbrc_flask.pytest.asserts import assert__input_text, assert__input_date, assert__input_radio
from lbrc_flask.pytest.testers import ResultHtmlType
from lbrc_flask.pytest.form_tester import FormTester, FormTesterTextField, FormTesterDateField, FormTesterRadioField


class PackViewTester:
    @property
    def item_creator(self):
        return self.faker.pack()

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

    @staticmethod
    def fields() -> FormTester:
        return FormTester([
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
                field_name='packtype',
                field_title='Packtype',
                is_mandatory=True,
            ),
        ])

    @property
    def result_html_type(self):
        return ResultHtmlType.MODAL

    def assert_form(self, resp):

        options = {pt.packtype_name: str(pt.id) for pt in self.standard_packtypes}

        assert__input_text(resp.soup, 'pack_identity')
        assert__input_date(resp.soup, 'pack_expiry')
        assert__input_radio(resp.soup, 'pack_type', options)
