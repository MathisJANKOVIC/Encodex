import requests
import random
import uuid
import urls
import standard

def test_rename_standard():
    created_std_res = requests.post(urls.CREATE_STANDARD, json=standard.create()).json()["encoding_standard"]

    rename_std_body = {
        "encoding_standard_id": created_std_res["id"],
        "new_name": str(uuid.uuid4())
    }
    renamed_std_res = requests.put(urls.RENAME_STANDARD, json=rename_std_body)
    assert renamed_std_res.status_code == 200, standard.wrong_status_code_message(renamed_std_res.status_code, 200)

    created_std_res["name"] = rename_std_body["new_name"]
    assert created_std_res == renamed_std_res.json()["encoding_standard"], "response encoding standard is not as expected after rename"

def test_rename_standard_with_existing_name():
    std1_response = requests.post(urls.CREATE_STANDARD, json=standard.create()).json()["encoding_standard"]
    std2_response = requests.post(urls.CREATE_STANDARD, json=standard.create()).json()["encoding_standard"]

    rename_std_body = {
        "encoding_standard_id": std2_response["id"],
        "new_name": std1_response["name"]
    }
    renamed_std_res = requests.put(urls.RENAME_STANDARD, json=rename_std_body)
    assert renamed_std_res.status_code == 422, standard.wrong_status_code_message(renamed_std_res.status_code, 422)

def test_rename_non_existing_standard():
    update_std_body = {
        "encoding_standard_id": random.randint(100, 100_000_000),
        "new_name": "non-existing-standard-name"
    }
    response = requests.put(urls.RENAME_STANDARD, json=update_std_body)
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)