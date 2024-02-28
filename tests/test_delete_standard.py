# import tests.standard as standard
# import requests
# import urls

# def test_delete_standard():
#     standard = standard.create()
#     requests.post(urls.CREATE_STANDARD, json=standard)

#     response = requests.delete(f"{urls.DELETE_STANDARD}/{standard['name']}/")
#     assert response.status_code == 200, standard.failure_message(response)

# def test_delete_not_existing_standard():
#     response = requests.delete(f"{urls.DELETE_STANDARD}/not-existing-standard/")
#     assert response.status_code == 404, standard.message(response)