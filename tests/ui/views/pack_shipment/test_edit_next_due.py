import pytest
from lbrc_flask.pytest.testers import RequiresLoginTester, FlaskViewLoggedInTester
from lbrc_flask.pytest.asserts import assert__refresh_response
from lbrc_flask.pytest.form_tester import FormTester, FormTesterDateField
from sqlalchemy import select
from coloprevent.model import PackShipment
from lbrc_flask.database import db
from tests.ui.views.pack_shipment import PackShipmentViewTester


class PackShipmentFormTester(FormTester):
    def __init__(self, has_csrf=False):
        super().__init__(
            fields=[
                FormTesterDateField(
                    field_name='next_due',
                    field_title='Next Due',
                ),
            ],
            has_csrf=has_csrf,
        )


class PackShipmentEditNextDueViewTester(PackShipmentViewTester):
    @property
    def endpoint(self):
        return 'ui.add_shipment_next_due'

    @pytest.fixture(autouse=True)
    def set_standard_sites(self, standard_sites):
        self.standard_sites = standard_sites

    @pytest.fixture(autouse=True)
    def set_existing(self, client, faker, set_standard_sites):
        self.existing_pack_shipment = faker.pack_shipment().get(save=True, site=self.standard_sites[1])
        self.parameters['id'] = self.existing_pack_shipment.id


class TestPackShipmentEditNextDueRequiresLogin(PackShipmentEditNextDueViewTester, RequiresLoginTester):
    ...


class TestPackShipmentEditNextDueGet(PackShipmentEditNextDueViewTester, FlaskViewLoggedInTester):
    @pytest.mark.app_crsf(True)
    def test__get__has_form(self):
        resp = self.get()

        PackShipmentFormTester(has_csrf=True).assert_all(resp)


class TestPackShipmentEditNextDuePost(PackShipmentEditNextDueViewTester, FlaskViewLoggedInTester):
    def test__post__valid(self):
        expected = self.item_creator.get(save=False, site=None)
        data = self.get_data_from_object(expected)

        resp = self.post(data)

        assert__refresh_response(resp)

        self.assert_db_count(1)

        actual = db.session.execute(select(PackShipment)).scalar()

        self.assert_actual_equals_expected(expected, actual)
