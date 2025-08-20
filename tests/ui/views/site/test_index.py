import pytest
from lbrc_flask.pytest.testers import IndexTester, RequiresLoginTester


class SiteIndexTester:
    @property
    def endpoint(self):
        return 'ui.site_home'


def pytest_generate_tests(metafunc):
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


class TestSiteIndex(SiteIndexTester, IndexTester):
    @pytest.mark.parametrize("item_count", ['a'], indirect=True)
    def test__get__no_filters(self, item_count):
        self.faker.site().get_list_in_db(item_count=item_count)
        self.get_index_and_assert_standards(expected_count=item_count)


class TestSiteIndexRequiresLogin(SiteIndexTester, RequiresLoginTester):
    pass