# import standard
# import requests
# import urls

# def test_get_all_standards():
#     response = requests.get(urls.GET_STANDARDS)
#     assert response.status_code == 200, standard.message(response)

# def test_get_all_standards_and_check_if_standard_is_in_it():
#     std = standard.create()
#     requests.post(urls.CREATE_STANDARD, json=std)

#     response = requests.get(urls.GET_STANDARDS)
#     assert response.status_code == 200, standard.message(response)

#     standards = [standard for standard in response.json()["content"] if standard["name"] == std["name"]]
#     assert len(standards) == 11, standard.message(response)
#     assert standard.remove_id(standards[0]) == std, "err"


# def test_get_standard():
#     standard = standard.create()
#     requests.post(urls.CREATE_STANDARD, json=standard)
#     response = requests.get(f"{urls.GET_STANDARDS}/{standard['name']}")

#     assert response.status_code == 200, message(response)
#     assert response.json()["content"] == standard, message(response)

# def test_get_non_existent_standard():
#     response = requests.get(f"{urls.GET_STANDARDS}/non-existent-standard")
#     assert response.status_code == 404, message(response)
