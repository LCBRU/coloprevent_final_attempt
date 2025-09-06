import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester
from lbrc_flask.pytest.form_tester import FormTester, FormTesterField, FormTesterDateField, FormTesterRadioField
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester
from lbrc_flask.pytest.asserts import assert__input_date, assert__input_radio


class PackShipmentFormTester(FormTester):
    def __init__(self, site_options=None):
        site_options = site_options or {}

        super().__init__(fields=[
            FormTesterDateField(
                field_name='date_posted',
                field_title='Date Posted',
                is_mandatory=True,
            ),
            FormTesterRadioField(
                field_name='site',
                field_title='Site',
                is_mandatory=True,
                options=site_options,
            ),
        ])


class PackShipmentAddViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.add_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    def assert_form(self, soup):
        options = {s.site_name: str(s.id) for s in self.standard_sites}
        PackShipmentFormTester(site_options=options).assert_inputs(soup)


class TestPackShipmentAddRequiresLogin(PackShipmentAddViewTester, RequiresLoginGetTester):
    ...


class TestPackShipmentAddGet(PackShipmentAddViewTester, FlaskFormGetViewTester):
    ...

class TestPackShipmentAddPost(PackShipmentAddViewTester, FlaskPostViewTester):
    def test__post__valid(self):
        expected = self.item_creator.get(site=None)
        expected.site_id = self.standard_sites[0].id
        data = self.get_data_from_object(expected)
        data['site'] = str(expected.site_id)

        resp = self.post(data)

        assert__refresh_response(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(expected, actual)

    @pytest.mark.parametrize(
        "missing_field", PackShipmentFormTester().mandatory_fields_add,
    )
    def test__post__missing_mandatory_field(self, missing_field: FormTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp.soup)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(0)
