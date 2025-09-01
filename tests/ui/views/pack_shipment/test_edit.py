import pytest
from lbrc_flask.pytest.testers import RequiresLoginGetTester, FlaskFormGetViewTester, FlaskPostViewTester, ModelTesterField
from lbrc_flask.pytest.asserts import assert__refresh_response
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester
from lbrc_flask.pytest.asserts import assert__input_date, assert__input_radio
from lbrc_flask.pytest.testers import ModelTesterField, ModelTesterField_DataType, ModelTesterFields


class PackShipmentAddViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.edit_shipment'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get_in_db(site=self.standard_sites[1])
        self.parameters = dict(id=self.existing_pack_shipment.id)

    @staticmethod
    def fields() -> ModelTesterFields:
        return ModelTesterFields([
            ModelTesterField(
                field_name='date_posted',
                field_title='Date Posted',
                data_type=ModelTesterField_DataType.DATE,
                is_mandatory=True,
            ),
            ModelTesterField(
                field_name='date_received',
                field_title='Date Received',
                data_type=ModelTesterField_DataType.DATE,
            ),
            ModelTesterField(
                field_name='next_due',
                field_title='Next Due',
                data_type=ModelTesterField_DataType.DATE,
            ),
            ModelTesterField(
                field_name='site',
                field_title='Site',
                data_type=ModelTesterField_DataType.RADIO,
                is_mandatory=True,
            ),
        ])

    def assert_form(self, resp):
        options = {s.site_name: str(s.id) for s in self.standard_sites}

        assert__input_date(resp.soup, 'date_posted')
        assert__input_date(resp.soup, 'date_received')
        assert__input_date(resp.soup, 'next_due')
        assert__input_radio(resp.soup, 'site', options)


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
        "missing_field", PackShipmentAddViewTester.fields().mandatory_fields_add,
    )
    def test__post__missing_mandatory_field(self, missing_field: ModelTesterField):
        expected = self.item_creator.get()
        data = self.get_data_from_object(expected)
        data[missing_field.field_name] = ''

        resp = self.post(data)

        self.assert_standards(resp)
        self.assert_form(resp)
        self.assert__error__required_field(resp, missing_field.field_title)
        self.assert_db_count(1)
