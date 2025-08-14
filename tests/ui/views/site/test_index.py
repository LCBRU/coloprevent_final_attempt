from flask import url_for
from lbrc_flask.pytest.asserts import assert__search_html, assert__requires_login
from tests.requests import coloprevents_catalogue_get
from lbrc_flask.pytest.html_content import get_records_found, get_panel_list_row_count


def _url(external=True, **kwargs):
    return url_for('ui.site_home', _external=external, **kwargs)


def _get(client, url, user, expected_count):
    resp = coloprevents_catalogue_get(client, url, user)

    assert__search_html(resp.soup, clear_url=_url(external=False))

    assert expected_count == get_records_found(resp.soup)
    assert expected_count == get_panel_list_row_count(resp.soup)

    return resp


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))


def test__get__one(client, faker, loggedin_user):
    specimen = faker.site().get_in_db()
    resp = _get(client, _url(), loggedin_user, expected_count=1)
