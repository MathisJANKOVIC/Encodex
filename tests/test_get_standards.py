# import tests.standard as standard
# from tests.standard import message
# import requests
# import urls

# def test_get_all_standards():
#     response = requests.get(urls.GET_STANDARDS)
#     assert response.status_code == 200, message(response)

# def test_get_all_standards_and_check_if_standard_is_in_it():
#     standard = standard.create()
#     requests.post(urls.CREATE_STANDARD, json=standard)

#     response = requests.get(urls.GET_STANDARDS)
#     response_std = [response_std for response_std in response.json()["content"] if response_std["name"] == standard["name"]]

#     assert response.status_code == 200, message(response)
#     assert len(response_std) == 1, message(response)
#     assert response_std[0] == standard, message(response)

# def test_get_standard():
#     standard = standard.create()
#     requests.post(urls.CREATE_STANDARD, json=standard)
#     response = requests.get(f"{urls.GET_STANDARDS}/{standard['name']}")

#     assert response.status_code == 200, message(response)
#     assert response.json()["content"] == standard, message(response)

# def test_get_non_existent_standard():
#     response = requests.get(f"{urls.GET_STANDARDS}/non-existent-standard")
#     assert response.status_code == 404, message(response)
