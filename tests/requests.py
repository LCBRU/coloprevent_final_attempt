from lbrc_flask.pytest.asserts import assert_html_page_standards, assert_modal_standards


def coloprevents_catalogue_get(client, url, user, has_form=False):
    resp = client.get(url)
    assert_html_page_standards(resp, user, has_form=has_form)

    return resp


def coloprevent_catalogue_modal_get(client, url, has_form=False):
    resp = client.get(url)
    assert_modal_standards(resp, has_form=has_form)

    return resp
