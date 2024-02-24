from encoding_standard import failure_message
import encoding_standard
import requests
import urls

def test_update_encoding_standard_with_new_encoding_char():
    standard = encoding_standard.create()
    requests.post(urls.CREATE, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"a": "z", "b": "x", "c": "y"}
    }

    response = requests.patch(urls.UPDATE, json=updated_standard)
    assert response.status_code == 200, failure_message(response)

def test_update_existing_encoding_char_in_encoding_standard():
    standard = encoding_standard.create(charset={"a": "A", "b": "B", "c": "C"})
    requests.post(urls.CREATE, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"d": "D", "e": "e", "f": "F"}
    }

    response = requests.patch(urls.UPDATE, json=updated_standard)
    assert response.status_code == 200, failure_message(response)

def test_update_not_existing_encoding_standard():
    standard = encoding_standard.create()
    requests.post(urls.CREATE, json=standard)

    updated_standard = {
        "encoding_standard_name": "not-existing-encoding-standard",
        "charset": {"!": "x"}
    }

    response = requests.patch(urls.UPDATE, json=updated_standard)
    assert response.status_code == 404, failure_message(response)