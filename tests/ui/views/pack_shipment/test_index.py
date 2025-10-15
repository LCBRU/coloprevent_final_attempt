import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginGetTester, PagedResultSet
from lbrc_flask.python_helpers import sort_descending


class PackShipmentIndexTester:
    @property
    def endpoint(self):
        return 'ui.index'


class TestPackShipmentIndex(PackShipmentIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", PagedResultSet.test_page_edges())
    @pytest.mark.parametrize("current_page", PagedResultSet.test_current_pages())
    def test__get__no_filters(self, item_count, current_page):
        pack_shiptments = self.faker.pack_shipment().get_list_in_db(item_count=item_count)
        pack_shipments = sorted(pack_shiptments, key=lambda x: (sort_descending(x.date_posted), sort_descending(x.id)))

        self.parameters['page'] = current_page

        resp = self.get()

        self.assert_all(
            page_count_helper=PagedResultSet(page=current_page, expected_results=pack_shiptments),
            resp=resp,
        )


class TestPackShipmentIndexRequiresLogin(PackShipmentIndexTester, RequiresLoginGetTester):
    ...
